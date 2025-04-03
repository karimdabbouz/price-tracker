import sys
from pathlib import Path

project_root = str(Path(__file__).parent.parent)
sys.path.append(project_root)

from db.models import Retailer
from schemas import RetailerConfig
import argparse
from db.database import Database
from logger import logger


def add_retailer(session, name, base_url, scraping_method='ui', scrape_interval=3600, affiliate_tag=None, selenium_mode='uc', selenium_headed=True, selenium_proxy=None):
    config = RetailerConfig(
        base_url=base_url,
        scraping_method=scraping_method,
        selenium_settings={
            'mode': selenium_mode,
            'headed': selenium_headed,
            'proxy': selenium_proxy
        }
    )
    
    retailer = Retailer(
        name=name,
        base_url=base_url,
        scraping_config=config.model_dump(),
        affiliate_tag=affiliate_tag,
        scrape_interval=scrape_interval
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
        logger.info(f'ID: {r.id}, Name: {r.name}, URL: {r.base_url}, Interval: {r.scrape_interval}')


def main():
    parser = argparse.ArgumentParser(description='Manage retailers in the database')
    parser.add_argument('action', choices=['add', 'list'], help='Action to perform')
    parser.add_argument('--name', help='Retailer name')
    parser.add_argument('--base-url', help='Retailer base URL')
    parser.add_argument('--scraping-method', default='ui', choices=['ui', 'api', 'sitemap'], help='Scraping method')
    parser.add_argument('--scrape-interval', type=int, default=3600, help='Scrape interval in seconds')
    parser.add_argument('--affiliate-tag', help='Affiliate tag')
    parser.add_argument('--selenium-mode', choices=['uc', 'wire'], default='uc', help='Selenium mode')
    parser.add_argument('--selenium-headed', type=bool, default=True, help='Run selenium in headed mode')
    parser.add_argument('--selenium-proxy', help='Proxy URL for selenium')
    
    args = parser.parse_args()
    db = Database()
    
    with db.get_session() as session:
        try:
            if args.action == 'add':
                if not args.name or not args.base_url:
                    logger.error('Error: --name and --base-url are required for "add" action')
                    return
                add_retailer(
                    session, 
                    args.name, 
                    args.base_url, 
                    args.scraping_method,
                    args.scrape_interval,
                    args.affiliate_tag,
                    args.selenium_mode,
                    args.selenium_headed,
                    args.selenium_proxy
                )
            elif args.action == 'list':
                list_retailers(session)
        except Exception as e:
            logger.error(f"Error: {str(e)}")


if __name__ == '__main__':
    main() 