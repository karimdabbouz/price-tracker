import datetime
from typing import Optional, List, Dict, Any
from sqlalchemy import or_, func, desc, asc
from sqlalchemy.orm import Session
from ..models import Product, Prices, Retailer
from shared.schemas import ProductSchema, ProductListingSchema, PriceSchema
from sqlalchemy.sql import nullslast


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


    def get_by_manufacturer(
        self, 
        manufacturer: str, 
        release_year: Optional[int] = None, 
        limit: Optional[int] = None,
        sort_by: Optional[str] = None,
        order: Optional[str] = 'desc'
    ) -> List[ProductSchema]:
        '''
        Returns a list of products for a given manufacturer with flexible filtering and sorting.
        
        Args:
            manufacturer: Name of the manufacturer
            release_year: Optional year to filter products by
            limit: Optional maximum number of products to return
            sort_by: Optional field to sort by (e.g., 'release_year', 'name', 'price')
            order: Optional sort order ('asc' or 'desc'), defaults to 'desc'
        '''
        print(f'Params: {manufacturer}, {release_year}, {limit}, {sort_by}, {order}')
        
        query = self.session.query(Product).filter(Product.manufacturer == manufacturer)
        if release_year:
            query = query.filter(Product.release_year == release_year)
        if sort_by:
            sort_column = getattr(Product, sort_by, None)
            if sort_column is not None:
                if order.lower() == 'desc':
                    query = query.order_by(nullslast(sort_column.desc()))
                else:
                    query = query.order_by(nullslast(sort_column.asc()))
        if limit:
            query = query.limit(limit)
        products = query.all()
        return [ProductSchema.model_validate(product.__dict__) for product in products]
    

    def get_by_manufacturer_v2(
        self, 
        manufacturer: str, 
        release_year: List[int] = [],
        limit: Optional[int] = None,
        offset: Optional[int] = 0,
        sort_by: Optional[str] = None,
        order: Optional[str] = 'desc'
    ) -> List[ProductListingSchema]:
        '''
        foo bar
        '''
        query = self.session.query(Product, func.count(Prices.id).label('num_prices'))
        query = query.filter(Product.manufacturer == manufacturer)
        query = query.join(Prices, (Product.id == Prices.product_id) & (Prices.in_stock == True))
        query = query.group_by(Product.id)
        if release_year:
            query = query.filter(Product.release_year.in_(release_year))
        query = query.order_by(desc('num_prices') if order == 'desc' else asc('num_prices'))
        if limit:
            query = query.limit(limit)
        if offset:
            query = query.offset(offset)
        products = query.all()




    # def get_by_manufacturer_v2(
    #     self, 
    #     manufacturer: str, 
    #     release_year: Optional[int] = None, 
    #     limit: Optional[int] = None,
    #     offset: Optional[int] = 0,
    #     sort_by: Optional[str] = None,
    #     order: Optional[str] = 'desc'
    # ) -> List[ProductListingSchema]:
    #     '''
    #     Returns a list of products for a given manufacturer with flexible filtering and sorting.
    #     '''
    #     query = self.session.query(Product).filter(Product.manufacturer == manufacturer)
    #     if release_year:
    #         query = query.filter(Product.release_year == release_year)
    #     if sort_by:
    #         sort_column = getattr(Product, sort_by, None)
    #         if sort_by == 'num_prices':
    #             price_count = func.count(Prices.id)
    #             query = query.outerjoin(Prices, Product.id == Prices.product_id)
    #             query = query.group_by(Product.id)
    #             sort_column = price_count
    #         if sort_column is not None:
    #             query = query.order_by(
    #                 desc(sort_column) if order == 'desc' else asc(sort_column)
    #             )
    #     if limit:
    #         query = query.limit(limit)
    #     if offset:
    #         query = query.offset(offset)
    #     products = query.all()
    #     # get prices now and assemble result
    #     product_listings = []
    #     for product in products:
    #         prices = self.session.query(Prices).filter_by(product_id=product.id).all()
    #         prices_in_stock = [p for p in prices if p.in_stock] # cant we do this before? what benefits do we get?
    #         if prices_in_stock:
    #             product_dict = {
    #                 'id': product.id,
    #                 'manufacturer_id': product.manufacturer_id,
    #                 'name': product.name,
    #                 'manufacturer': product.manufacturer,
    #                 'category': product.category,
    #                 'base_image_url': product.base_image_url,
    #                 'description': product.description,
    #                 'release_year': product.release_year,
    #                 'prices': [PriceSchema.model_validate(price.__dict__) for price in prices_in_stock]
    #             }
    #             product_listings.append(ProductListingSchema(**product_dict))
    #     return product_listings
            

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