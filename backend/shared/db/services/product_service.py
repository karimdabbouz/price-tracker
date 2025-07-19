import datetime
from typing import Optional, List, Dict, Any, Tuple
from sqlalchemy import or_, func, desc # type: ignore
from sqlalchemy.orm import Session # type: ignore
from ..models import Product, Prices, Retailer
from shared.schemas import ProductSchema, ProductListingSchema, PriceSchema
import logging

logger = logging.getLogger(__name__)

class ProductService:
    '''
    Service for handling Product-related database operations.
    '''
    def __init__(self, session: Session):
        self.session = session
    

    def get_by_id(self, id: int) -> ProductSchema:
        '''
        Gets a product by its ID.
        '''
        product = self.session.query(Product).filter(Product.id == id).first()
        return ProductSchema.model_validate(product.__dict__)
    

    def get_available_products_by_manufacturer(
        self, 
        manufacturer: str, 
        release_year: List[int] = [],
        limit: Optional[int] = None,
        offset: Optional[int] = 0
    ) -> Tuple[List[ProductListingSchema], int]:
        '''
        Gets products for which at least one price exists by manufacturer
        using limit and offset for one or more specified release years.

        Used in /manufacturers/{manufacturer}/product_listings API endpoint for the /marken/[manufacturer] route.
        
        Args:
            manufacturer: The manufacturer
            release_year: One or more release years to filter by
            limit: Optional max number of results to return
            offset: Optional offset
        '''
        query = self.session.query(Product, func.count(Prices.id).label('num_prices'))
        query = query.filter(Product.manufacturer == manufacturer)
        query = query.join(Prices, (Product.id == Prices.product_id) & (Prices.in_stock == True))
        if release_year:
            query = query.filter(Product.release_year.in_(release_year))
        query = query.group_by(Product.id)
        total_count = query.count()

        query = query.order_by(desc('num_prices'))
        if limit:
            query = query.limit(limit)
        if offset:
            query = query.offset(offset)
        products = query.all()

        product_ids = [product.id for product, _ in products]
        if not product_ids:
            return [], total_count
        prices = self.session.query(Prices).filter(Prices.product_id.in_(product_ids), Prices.in_stock == True).all()

        prices_by_product = {}
        for price in prices:
            prices_by_product.setdefault(price.product_id, []).append(PriceSchema.model_validate(price.__dict__))

        product_listings = []
        for product, num_prices in products:
            in_stock_prices = prices_by_product.get(product.id, [])
            if in_stock_prices:
                product_dict = {
                    'id': product.id,
                    'manufacturer_id': product.manufacturer_id,
                    'name': product.name,
                    'manufacturer': product.manufacturer,
                    'category': product.category,
                    'base_image_url': product.base_image_url,
                    'description': product.description,
                    'release_year': product.release_year,
                    'prices': in_stock_prices
                }
                product_listings.append(ProductListingSchema.model_validate(product_dict))
        return product_listings, total_count


    def get_autocomplete(self) -> List[Dict[str, Any]]:
        '''
        Returns a list of product manufacturer, name and id for autocomplete.
        '''
        return [
            {'id': p.id, 'manufacturer': p.manufacturer, 'name': p.name}
            for p in self.session.query(Product.id, Product.manufacturer, Product.name).all()
        ]
    

    def get_products_to_scrape(self, scrape_interval: tuple[str, int], retailer_id: int) -> List[ProductSchema]:
        '''
        Returns a list of products that need to be scraped for this retailer:
        Filters products by release_year depending on the first value in scrape_interval (current_year, previous_year, older).
        Excludes products by excluded brands set in retailer.
        Gets products where there is no price at all for this retailer or the last price was updated more than interval_duration seconds ago.

        Args:
            scrape_ interval: Tuple of interval_name (current_year, previous_year, older) and interval to check for new prices again (in seconds)
            retailer_id: The ID of the retailer to check prices for
        '''
        interval_name, interval_duration = scrape_interval
        current_year = datetime.datetime.now().year
        
        retailer = self.session.query(Retailer).filter(Retailer.id == retailer_id).first()
        excluded_brands = retailer.excluded_brands
        
        if interval_name == 'current_year':
            year_filter = Product.release_year == current_year
        elif interval_name == 'previous_year':
            year_filter = Product.release_year == current_year - 1
        else: # older
            year_filter = Product.release_year < current_year - 1
        
        products = self.session.query(Product).outerjoin(
            Prices,
            (Product.id == Prices.product_id) & (Prices.retailer_id == retailer_id)
        ).filter(
            year_filter,
            ~Product.manufacturer.in_(excluded_brands),
            or_(
                Prices.id == None,
                Prices.last_updated < datetime.datetime.now() - datetime.timedelta(seconds=interval_duration)
            )
        ).all()
        
        return [ProductSchema.model_validate(product.__dict__) for product in products]


    def update_entry(self, product_id: int, updates: Dict[str, Any]) -> Optional[ProductSchema]:
        '''
        Updates a product entry in the products table. When changing a value, the created_at value is updated to now.
        
        Returns the updated ProductSchema or none if nothing has changed.
        
        Args:
            product_id: The ID of the product to update
            updates: A dict of fields to update (e.g., {'name': 'New Name'})
        '''
        logger.info(f'Called update_entry for product_id={product_id} with updates={updates}')
        product = self.session.query(Product).filter(Product.id == product_id).first()
        if not product:
            logger.warning(f'No product found with id={product_id}')
            return None
        for key, value in updates.items():
            if hasattr(product, key):
                logger.info(f'Updating {key} from {getattr(product, key)} to {value}')
                setattr(product, key, value)
        product.created_at = datetime.datetime.now(datetime.UTC)
        self.session.commit()
        return ProductSchema.model_validate(product.__dict__)