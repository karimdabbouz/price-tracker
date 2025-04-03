from typing import Optional
from sqlalchemy.orm import Session
from ..models import Product
from schemas import ProductSchema


class ProductService:
    '''
    Service for handling Product-related database operations.
    '''
    def __init__(self, session: Session):
        self.session = session
    

    def update(self, product_id: int, product_data: ProductSchema) -> Optional[Product]:
        '''
        Update an existing product.
        
        Args:
            product_id: ID of the product to update
            product_data: Pydantic schema with updated data
            
        Returns:
            Updated Product if found, None otherwise
        '''
        product = self.session.query(Product).filter(Product.id == product_id).first()
        if product:
            update_data = product_data.model_dump(exclude={'id'})
            for key, value in update_data.items():
                setattr(product, key, value)
            self.session.commit()
        return product


    def get_by_id():
        '''
        Just an example for later
        '''
        pass