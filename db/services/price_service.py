from typing import Optional
from sqlalchemy.orm import Session
from ..models import Prices
from schemas import PriceSchema
import datetime


class PriceService:
    '''
    Service for handling Price-related database operations.
    '''
    
    def __init__(self, session: Session):
        self.session = session


    def price_exists(self, product_id: int, retailer_id: int) -> bool:
        '''
        Checks if a price entry exists for the given product and retailer.
        
        Args:
            product_id: Product ID
            retailer_id: Retailer ID
            
        Returns:
            bool: True if price exists, False otherwise
        '''
        return self.session.query(Prices).filter_by(
            product_id=product_id,
            retailer_id=retailer_id
        ).first() is not None
    

    def add_price(self, price_schema: PriceSchema) -> Prices:
        '''
        Creates a new price entry.
        
        Args:
            price_schema: PriceSchema object
            
        Returns:
            Created Prices database object
        '''
        price_data = price_schema.model_dump(exclude={'id'})
        price_data['last_updated'] = datetime.datetime.now(datetime.UTC)
        new_price = Prices(**price_data)
        self.session.add(new_price)
        self.session.commit()
        return new_price
    

    def update_price(self, price_schema: PriceSchema) -> Optional[Prices]:
        '''
        Updates an existing price entry and tracks price history.
        
        Args:
            price_schema: Validated PriceSchema object
            
        Returns:
            Updated Prices database object if found, None otherwise
        '''
        existing_price = self.session.query(Prices).filter_by(
            product_id=price_schema.product_id,
            retailer_id=price_schema.retailer_id
        ).first()
        
        if not existing_price:
            return None
            
        # Only update if price has changed
        if existing_price.price != price_schema.price:
            history = existing_price.price_history or []
            history.append({
                'price': existing_price.price,
                'datetime': existing_price.last_updated.isoformat()
            })
            price_schema.price_history = history
            
            # Update only changed fields
            existing_price.price = price_schema.price
            existing_price.price_history = price_schema.price_history
            existing_price.last_updated = datetime.datetime.now(datetime.UTC)
            self.session.commit()
            return existing_price
            
        return None  # Return None if no changes were made