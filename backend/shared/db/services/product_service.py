import datetime
from typing import Optional, List, Dict, Any
from sqlalchemy import or_, func
from sqlalchemy.orm import Session
from ..models import Product, Prices, Retailer
from shared.schemas import ProductSchema


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


    def get_by_manufacturer(self, manufacturer: str, release_year: Optional[int] = None, limit: Optional[int] = None) -> List[ProductSchema]:
        '''
        Returns a list of products for a given manufacturer.
        
        Args:
            manufacturer: Name of the manufacturer
            release_year: Optional year to filter products by
            limit: Optional maximum number of products to return
        '''
        if release_year:
            query = self.session.query(Product).filter(Product.manufacturer == manufacturer, Product.release_year == release_year)
        else:
            query = self.session.query(Product).filter(Product.manufacturer == manufacturer)
        if limit:
            query = query.limit(limit)
        products = query.all()
        return [ProductSchema.model_validate(product.__dict__) for product in products]
    

    def get_autocomplete(self) -> List[Dict[str, Any]]:
        '''
        Returns a list of product manufacturer, name and id for autocomplete.
        '''
        return [
            {'id': p.id, 'manufacturer': p.manufacturer, 'name': p.name}
            for p in self.session.query(Product.id, Product.manufacturer, Product.name).all()
        ]
    

    def get_products_to_scrape(self, interval: tuple[str, int], retailer_id: int) -> List[ProductSchema]:
        '''
        Returns a list of products that need to be scraped.

        Args:
            interval: Tuple of (interval_name, interval_duration)
            retailer_id: The ID of the retailer to check prices for.
        '''
        interval_name, interval_duration = interval
        current_year = datetime.datetime.now().year
        
        retailer = self.session.query(Retailer).filter(Retailer.id == retailer_id).first()
        excluded_brands = retailer.excluded_brands
        
        if interval_name == 'current_year':
            year_filter = Product.release_year == current_year
        elif interval_name == 'previous_year':
            year_filter = Product.release_year == current_year - 1
        else:
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