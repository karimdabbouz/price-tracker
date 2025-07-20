from sqlalchemy.orm import Session
from ..models import ProductContent


class ProductContentService:
    def __init__(self, session: Session):
        self.session = session

    def get_product_ids_with_content_type(self, content_type: str):
        '''
        Returns a set of product IDs that have at least one ProductContent entry with the given content_type.
        Args:
            content_type: The content_type string to filter by (e.g., 'foreign_review')
        Returns:
            Set of product IDs
        '''
        results = self.session.query(ProductContent.product_id).filter(ProductContent.content_type == content_type).distinct().all()
        return set(r[0] for r in results)