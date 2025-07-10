import sys, random
from pathlib import Path
from apscheduler.schedulers.blocking import BlockingScheduler # type: ignore
from apscheduler.triggers.interval import IntervalTrigger # type: ignore
from dotenv import load_dotenv
from typing import List

project_root = str(Path(__file__).parent.parent.parent.parent)
sys.path.append(project_root)

from shared.db.services.product_service import ProductService
from shared.db.services.retailer_service import RetailerService
from shared.db.database import Database
from shared.db.services.price_service import PriceService
from scraping.scrapers.spielzeug_fuchs.spielzeugfuchs_scraper import SpielzeugFuchsScraper
from shared.schemas import ProductSchema, RetailerSchema
from shared.logger import logger


load_dotenv()


retailer_id = 6


def scrape_job(scrape_interval: tuple[str, int], product_service: ProductService, price_service: PriceService, scraper: SpielzeugFuchsScraper):
    '''
    Does the actual scraping.

    Args:
        scrape_interval: The interval to scrape the prices taken from retailer (interval_name, interval_duration).
        product_service: The product service to use.
        scraper: The scraper instance to use.
    '''
    products: List[ProductSchema] = product_service.get_products_to_scrape(scrape_interval, retailer_id)
    logger.info(f'Run for products for {scrape_interval[0]} - {scrape_interval[1]}')
    logger.info(f'{len(products)} products found for this run in db')
    results = scraper.run(products)
    logger.info(f'{len(results)} prices found by scraper')
    for result in results:
        try:
            if price_service.price_exists(result.product_id, result.retailer_id):
                updated_price = price_service.update_price(result)
                if updated_price:
                    logger.info(f'Updated price for product {result.product_id}')
            else:
                price_service.add_price(result)
                logger.info(f'Added new price for product {result.product_id}')
        except Exception as e:
            logger.error(f'Error updating price for product {result.product_id}: {e}')


def run_scraper():
    '''
    Sets the scheduler and runs the scraper for the retailer id specified at the top.
    '''
    scheduler = BlockingScheduler()

    db = Database()

    with db.get_session() as session:
        retailer_service = RetailerService(session)
        product_service = ProductService(session)
        price_service = PriceService(session)
        retailer: RetailerSchema = retailer_service.get_by_id(retailer_id)
        scraper = SpielzeugFuchsScraper(retailer.scraping_config)
        sample_interval = retailer.scrape_intervals.items()
        products = product_service.get_products_to_scrape(list(sample_interval)[0], 6)
        sample_products = random.choices(products, k=2)
        results = scraper.run(sample_products)
        print(results)



    # with db.get_session() as session:
    #     retailer_service = RetailerService(session)
    #     product_service = ProductService(session)
    #     price_service = PriceService(session)
    #     retailer: RetailerSchema = retailer_service.get_by_id(retailer_id)
    #     scrape_interval = retailer.scrape_intervals
    #     for k, v in scrape_interval.items():
    #         scraper = SpielzeugFuchsScraper(retailer.scraping_config)
    #         scheduler.add_job(
    #             lambda scrape_interval=(k, v), scraper=scraper: scrape_job(scrape_interval, product_service, price_service, scraper),
    #             trigger=IntervalTrigger(seconds=v),
    #             id=f'spielzeugfuchs_scraper_{k}',
    #             name=f'SpielzeugFuchs Price Scraper ({v}s)',
    #             replace_existing=True
    #         )
    # scheduler.start()


if __name__ == '__main__':
    run_scraper()
