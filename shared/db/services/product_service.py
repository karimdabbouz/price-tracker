from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from ..models import Product
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
        Returns a list of product names and id for autocomplete.
        '''
        return [
            {'id': p.id, 'name': p.name}
            for p in self.session.query(Product.id, Product.name).all()
        ]