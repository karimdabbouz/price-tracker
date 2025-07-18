from sqlalchemy.orm import Session


class ProductContentService:
    def __init__(self, session: Session):
        self.session = session

    pass 