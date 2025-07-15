import datetime
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Text, JSON, UniqueConstraint, Float, Boolean # type: ignore
from sqlalchemy.ext.declarative import declarative_base # type: ignore
from sqlalchemy.dialects.postgresql import ARRAY
from pgvector.sqlalchemy import Vector  # Add this import

Base = declarative_base()

class Product(Base):
    __tablename__ = 'products'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    manufacturer_id = Column(String)
    name = Column(String)
    manufacturer = Column(String)
    category = Column(String)
    base_image_url = Column(String)
    description = Column(Text)
    piece_count = Column(Integer)
    minifigures = Column(Integer)
    release_year = Column(Integer)
    created_at = Column(DateTime, default=datetime.datetime.now(datetime.UTC))

class Prices(Base):
    __tablename__ = 'prices'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey('products.id'))
    retailer_id = Column(Integer, ForeignKey('retailers.id'))
    price = Column(Float)
    shipping_cost = Column(Float)
    in_stock = Column(Boolean)
    url = Column(String)
    last_updated = Column(DateTime, default=datetime.datetime.now(datetime.UTC), index=True)
    price_history = Column(JSON)

    __table_args__ = (
        UniqueConstraint('product_id', 'retailer_id', name='uix_product_retailer'),
    )

class Retailer(Base):
    __tablename__ = 'retailers'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True)
    base_url = Column(String)
    scraping_config = Column(JSON)
    affiliate_tag = Column(String)
    scrape_intervals = Column(JSON)
    excluded_brands = Column(JSON)  # List of brand names to exclude
    base_image_url = Column(String)

class ProductContent(Base):
    __tablename__ = 'product_content'

    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False, index=True)
    content_type = Column(String, nullable=False)  # e.g., 'ai_description', 'pros_cons', 'faq'
    content = Column(JSON, nullable=False)         # Structured content (dict or list)
    embedding = Column(Vector(384), nullable=True) # Vector embedding (384 dims as a placeholder for now)
    created_at = Column(DateTime, default=datetime.datetime.now(datetime.UTC))
    updated_at = Column(DateTime, default=datetime.datetime.now(datetime.UTC), onupdate=datetime.datetime.now(datetime.UTC))

    __table_args__ = (
        UniqueConstraint('product_id', 'content_type', 'content', name='uix_product_content_unique'),
    )