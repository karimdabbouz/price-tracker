import sys
from pathlib import Path

project_root = str(Path(__file__).parent.parent)
sys.path.append(project_root)

from shared.db.models import Retailer
from shared.schemas import RetailerConfig
import argparse
from shared.db.database import Database
from shared.logger import logger


def add_retailer(session, name, base_url, scraping_method='ui', scrape_intervals=None, affiliate_tag=None, selenium_mode='uc', selenium_headed=True, selenium_proxy=None, excluded_brands=None):
    config = RetailerConfig(
        base_url=base_url,
        scraping_method=scraping_method,
        selenium_settings={
            'mode': selenium_mode,
            'headed': selenium_headed,
            'proxy': selenium_proxy
        }
    )
    
    # Default intervals if none provided
    if scrape_intervals is None:
        scrape_intervals = {
            'current_year': 6 * 3600,    # 6 hours
            'previous_year': 12 * 3600,  # 12 hours
            'older': 24 * 3600          # 24 hours
        }
    
    retailer = Retailer(
        name=name,
        base_url=base_url,
        scraping_config=config.model_dump(),
        affiliate_tag=affiliate_tag,
        scrape_intervals=scrape_intervals,
        excluded_brands=excluded_brands or []
    )
    session.add(retailer)
    session.commit()
    
    # Update scraping_config with the actual retailer_id
    config.id = retailer.id
    retailer.scraping_config = config.model_dump()
    session.commit()
    
    logger.info(f'Added retailer: {name} (ID: {retailer.id})')


def list_retailers(session):
    retailers = session.query(Retailer).all()
    logger.info('\nCurrent retailers:')
    for r in retailers:
        logger.info(f'ID: {r.id}, Name: {r.name}, URL: {r.base_url}, Interval: {r.scrape_intervals}')


def main():
    parser = argparse.ArgumentParser(description='Manage retailers in the database')
    parser.add_argument('action', choices=['add', 'list'], help='Action to perform')
    parser.add_argument('--name', help='Retailer name')
    parser.add_argument('--base-url', help='Retailer base URL')
    parser.add_argument('--scraping-method', default='ui', choices=['ui', 'api', 'sitemap'], help='Scraping method')
    parser.add_argument('--current-year-interval', type=int, help='Scrape interval for current year products in hours')
    parser.add_argument('--previous-year-interval', type=int, help='Scrape interval for previous year products in hours')
    parser.add_argument('--older-interval', type=int, help='Scrape interval for older products in hours')
    parser.add_argument('--affiliate-tag', help='Affiliate tag')
    parser.add_argument('--selenium-mode', choices=['uc', 'wire'], default='uc', help='Selenium mode')
    parser.add_argument('--selenium-headed', type=bool, default=True, help='Run selenium in headed mode')
    parser.add_argument('--selenium-proxy', help='Proxy URL for selenium')
    parser.add_argument('--excluded-brands', nargs='+', help='List of brands to exclude from scraping')
    args = parser.parse_args()
    db = Database()
    
    with db.get_session() as session:
        try:
            if args.action == 'add':
                if not args.name or not args.base_url:
                    logger.error('Error: --name and --base-url are required for "add" action')
                    return
                
                scrape_intervals = {}
                if args.current_year_interval:
                    scrape_intervals['current_year'] = args.current_year_interval * 3600
                if args.previous_year_interval:
                    scrape_intervals['previous_year'] = args.previous_year_interval * 3600
                if args.older_interval:
                    scrape_intervals['older'] = args.older_interval * 3600
                
                add_retailer(
                    session, 
                    args.name, 
                    args.base_url, 
                    args.scraping_method,
                    scrape_intervals if scrape_intervals else None,
                    args.affiliate_tag,
                    args.selenium_mode,
                    args.selenium_headed,
                    args.selenium_proxy,
                    args.excluded_brands
                )
            elif args.action == 'list':
                list_retailers(session)
        except Exception as e:
            logger.error(f"Error: {str(e)}")


if __name__ == '__main__':
    main() 