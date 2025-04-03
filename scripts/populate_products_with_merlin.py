import sys, os
from pathlib import Path

project_root = str(Path(__file__).parent.parent)
sys.path.append(project_root)

from logger import logger
from scripts.merlin_product_scraper import MerlinProductScraper
from db.database import Database
from db.models import Product
from sqlalchemy.exc import IntegrityError


def populate_products(merlin_url: str):
    """
    Populates the products table with initial data from Merlin
    """
    db = Database()
    db.init_db()
    
    # Initialize scraper
    scraper = MerlinProductScraper(merlin_url)
    
    # Get products
    products = scraper.scrape()
    
    with db.get_session() as session:
        success_count = 0
        error_count = 0
        
        for product in products:
            try:
                # Check if product with same manufacturer_id exists
                existing_product = session.query(Product).filter_by(manufacturer_id=product.manufacturer_id).first()
                if existing_product:
                    logger.info(f"Skipping duplicate manufacturer_id: {product.manufacturer_id}")
                    continue
                    
                # Check if product with same name exists
                existing_name = session.query(Product).filter_by(name=product.name).first()
                if existing_name:
                    logger.info(f"Skipping duplicate name: {product.name}")
                    continue

                db_product = Product(
                    manufacturer_id=product.manufacturer_id,
                    name=product.name,
                    manufacturer=product.manufacturer,
                    piece_count=product.piece_count,
                    release_year=product.release_year,
                    created_at=product.created_at
                )
                session.add(db_product)
                success_count += 1
            except IntegrityError:
                session.rollback()
                continue
            except Exception as e:
                logger.error(f"Error storing product {product.manufacturer_id}: {str(e)}")
                session.rollback()
                error_count += 1
    
    logger.info(f"Successfully stored {success_count} products")
    logger.info(f"Failed to store {error_count} products")
    if scraper.errors:
        logger.error("\nScraping errors:")
        for error in scraper.errors:
            logger.error(f"- {error}")

if __name__ == "__main__":
    MERLIN_URL = os.getenv("MERLIN_URL")
    if not MERLIN_URL:
        print("Error: MERLIN_URL environment variable is required")
        sys.exit(1)
        
    populate_products(MERLIN_URL) 