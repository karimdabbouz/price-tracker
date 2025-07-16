from sqlalchemy.orm import Session


class ProductDataService:
    def __init__(self, session: Session):
        self.session = session

    pass 