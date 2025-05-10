import sys
from pathlib import Path

project_root = str(Path(__file__).parent.parent)
sys.path.append(project_root)

from shared.db.models import Retailer
from shared.schemas import RetailerConfig
import argparse
from shared.db.database import Database
from shared.logger import logger


def add_retailer(session, name, base_url, scraping_method='ui', scrape_intervals=None, affiliate_tag=None, selenium_mode='uc', selenium_headed=True, selenium_proxy=None, excluded_brands=None, take_screenshots=False, base_image_url=None):
    config = RetailerConfig(
        base_url=base_url,
        scraping_method=scraping_method,
        take_screenshots=take_screenshots,
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
        excluded_brands=excluded_brands or [],
        base_image_url=base_image_url
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


def update_retailer(session, retailer_id, **kwargs):
    '''
    Update a retailer's configuration.
    
    Args:
        session: Database session
        retailer_id: ID of the retailer to update
        **kwargs: Fields to update (name, base_url, scraping_method, etc.)
    '''
    retailer = session.query(Retailer).filter(Retailer.id == retailer_id).first()
    if not retailer:
        logger.error(f'Retailer with ID {retailer_id} not found')
        return

    # Update basic fields
    if 'name' in kwargs:
        retailer.name = kwargs['name']
    if 'base_url' in kwargs:
        retailer.base_url = kwargs['base_url']
    if 'affiliate_tag' in kwargs:
        retailer.affiliate_tag = kwargs['affiliate_tag']
    if 'excluded_brands' in kwargs:
        retailer.excluded_brands = kwargs['excluded_brands']

    # Update scraping_config
    if any(k in kwargs for k in ['scraping_method', 'take_screenshots', 'selenium_mode', 'selenium_headed', 'selenium_proxy']):
        config = RetailerConfig.model_validate(retailer.scraping_config)
        
        if 'scraping_method' in kwargs:
            config.scraping_method = kwargs['scraping_method']
        if 'take_screenshots' in kwargs:
            config.take_screenshots = kwargs['take_screenshots']
        if any(k in kwargs for k in ['selenium_mode', 'selenium_headed', 'selenium_proxy']):
            if 'selenium_mode' in kwargs:
                config.selenium_settings['mode'] = kwargs['selenium_mode']
            if 'selenium_headed' in kwargs:
                config.selenium_settings['headed'] = kwargs['selenium_headed']
            if 'selenium_proxy' in kwargs:
                config.selenium_settings['proxy'] = kwargs['selenium_proxy']
        
        retailer.scraping_config = config.model_dump()

    # Update scrape_intervals
    if any(k in kwargs for k in ['current_year_interval', 'previous_year_interval', 'older_interval']):
        intervals = retailer.scrape_intervals or {}
        if 'current_year_interval' in kwargs:
            intervals['current_year'] = kwargs['current_year_interval'] * 3600
        if 'previous_year_interval' in kwargs:
            intervals['previous_year'] = kwargs['previous_year_interval'] * 3600
        if 'older_interval' in kwargs:
            intervals['older'] = kwargs['older_interval'] * 3600
        retailer.scrape_intervals = intervals

    if 'base_image_url' in kwargs:
        retailer.base_image_url = kwargs['base_image_url']

    session.commit()
    logger.info(f'Updated retailer: {retailer.name} (ID: {retailer.id})')


def main():
    parser = argparse.ArgumentParser(description='Manage retailers in the database')
    parser.add_argument('action', choices=['add', 'list', 'update'], help='Action to perform')
    parser.add_argument('--id', type=int, help='Retailer ID (required for update)')
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
    parser.add_argument('--take-screenshots', type=str, choices=['True', 'False'], help='Take screenshots during scraping (True/False)')
    parser.add_argument('--base-image-url', help='Base image URL for the retailer')
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
                    args.excluded_brands,
                    args.take_screenshots.lower() == 'true',
                    args.base_image_url
                )
            elif args.action == 'list':
                list_retailers(session)
            elif args.action == 'update':
                if not args.id:
                    logger.error('Error: --id is required for "update" action')
                    return
                
                update_kwargs = {}
                if args.name: update_kwargs['name'] = args.name
                if args.base_url: update_kwargs['base_url'] = args.base_url
                if args.scraping_method: update_kwargs['scraping_method'] = args.scraping_method
                if args.current_year_interval: update_kwargs['current_year_interval'] = args.current_year_interval
                if args.previous_year_interval: update_kwargs['previous_year_interval'] = args.previous_year_interval
                if args.older_interval: update_kwargs['older_interval'] = args.older_interval
                if args.affiliate_tag: update_kwargs['affiliate_tag'] = args.affiliate_tag
                if args.selenium_mode: update_kwargs['selenium_mode'] = args.selenium_mode
                if args.selenium_headed is not None: update_kwargs['selenium_headed'] = args.selenium_headed
                if args.selenium_proxy: update_kwargs['selenium_proxy'] = args.selenium_proxy
                if args.excluded_brands: update_kwargs['excluded_brands'] = args.excluded_brands
                if args.take_screenshots is not None: 
                    update_kwargs['take_screenshots'] = args.take_screenshots.lower() == 'true'
                if args.base_image_url: update_kwargs['base_image_url'] = args.base_image_url
                
                update_retailer(session, args.id, **update_kwargs)
        except Exception as e:
            logger.error(f"Error: {str(e)}")


if __name__ == '__main__':
    main() 