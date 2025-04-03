from typing import Optional
from sqlalchemy.orm import Session
from ..models import Retailer
from schemas import RetailerSchema


class RetailerService:
    '''
    Service for handling Retailer-related database operations.
    '''
    
    def __init__(self, session: Session):
        self.session = session
    
    
    def update(self, retailer_id: int, retailer_data: RetailerSchema) -> Optional[Retailer]:
        '''
        Update an existing retailer entry.
        
        Args:
            retailer_id: ID of the retailer to update
            retailer_data: Pydantic schema with updated data
            
        Returns:
            Updated Retailer if found, None otherwise
        '''
        retailer = self.session.query(Retailer).filter(Retailer.id == retailer_id).first()
        if retailer:
            update_data = retailer_data.model_dump(exclude={'id'})
            for key, value in update_data.items():
                setattr(retailer, key, value)
            self.session.commit()
        return retailer 