from contextlib import contextmanager
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from .models import Base
import os
from dotenv import load_dotenv
from logger import logger


class Database:
    '''
    Database connection manager that handles SQLAlchemy session lifecycle.
    
    Exposes a context manager for handling database sessions with automatic commit/rollback
    and cleanup.
    '''
    def __init__(self):
        load_dotenv()
        self.connection_string = os.getenv('DATABASE_URL')
        if not self.connection_string:
            logger.error('DATABASE_URL not found in environment variables')
            raise ValueError('DATABASE_URL not found in environment variables')
        self.engine = create_engine(self.connection_string)
        self.Session = sessionmaker(bind=self.engine)
    
    def init_db(self):
        logger.info("Initializing database")
        Base.metadata.create_all(self.engine)
    
    @contextmanager
    def get_session(self) -> Generator[Session, None, None]:
        session = self.Session()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close() 