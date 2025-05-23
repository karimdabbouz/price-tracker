from typing import Optional, List
from sqlalchemy.orm import Session # type: ignore
from ..models import Retailer
from shared.schemas import RetailerSchema


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
    

    def get_by_id(self, retailer_id: int) -> Optional[RetailerSchema]:
        '''
        Get a retailer by ID.
        '''
        retailer = self.session.query(Retailer).filter(Retailer.id == retailer_id).first()
        return RetailerSchema.model_validate(retailer.__dict__) if retailer else None


    def get_all(self) -> List[RetailerSchema]:
        '''
        Returns all retailers.
        '''
        retailers = self.session.query(Retailer).all()
        return [
            RetailerSchema.model_validate({
                'id': r.id,
                'name': r.name,
                'base_url': r.base_url,
                'scraping_config': r.scraping_config,
                'affiliate_tag': r.affiliate_tag,
                'scrape_intervals': r.scrape_intervals,
                'excluded_brands': r.excluded_brands,
                'base_image_url': r.base_image_url
            })
            for r in retailers
        ]
