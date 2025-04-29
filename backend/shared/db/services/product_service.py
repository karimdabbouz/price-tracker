import datetime
from typing import Optional, List, Dict, Any, Tuple
from sqlalchemy import or_, func, desc # type: ignore
from sqlalchemy.orm import Session # type: ignore
from ..models import Product, Prices, Retailer
from shared.schemas import ProductSchema, ProductListingSchema, PriceSchema


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
        Gets products for which at least one price exist by manufacturer
        using limit and offset for one or more specified release years.
        
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