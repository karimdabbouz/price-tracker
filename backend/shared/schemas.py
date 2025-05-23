import datetime
from pydantic import BaseModel, field_validator, ConfigDict
from typing import Optional, Dict, Any, List, Tuple


class ProductSchema(BaseModel):
    id: Optional[int] = None
    manufacturer_id: Optional[str] = None
    name: Optional[str] = None
    manufacturer: Optional[str] = None
    category: Optional[str] = None
    base_image_url: Optional[str] = None
    description: Optional[str] = None
    piece_count: Optional[int] = None
    minifigures: Optional[int] = None
    release_year: Optional[int] = None
    created_at: Optional[datetime.datetime] = None

    @classmethod
    def from_merlin_product(cls, data: list):
        return cls(
            id=None,
            manufacturer_id=data[1],
            name=data[3],
            manufacturer=data[2],
            category=None,
            base_image_url=None,
            description=None,
            piece_count=data[7],
            minifigures=None,
            release_year=data[8],
            created_at=datetime.datetime.now(datetime.UTC)
        )

    @field_validator('piece_count', mode='before')
    @classmethod
    def empty_string_to_none(cls, v):
        if isinstance(v, list):
            return None
        elif v == '':
            return None
        else:
            return v

    @field_validator('release_year', mode='before')
    @classmethod
    def release_year_to_int(cls, v):
        if isinstance(v, str):
            return None
        else:
            return v

    model_config = ConfigDict(coerce_numbers_to_str=True)


class PriceHistory(BaseModel):
    history: List[Tuple[datetime.datetime, float]] = []


class PriceSchema(BaseModel):
    id: Optional[int] = None
    product_id: Optional[int] = None
    retailer_id: Optional[int] = None
    price: Optional[float] = None
    shipping_cost: Optional[float] = None
    in_stock: Optional[bool] = None
    url: Optional[str] = None
    last_updated: Optional[datetime.datetime] = None
    price_history: Optional[PriceHistory] = None

    @field_validator('price_history', mode='before')
    @classmethod
    def parse_price_history(cls, v):
        if v:
            return PriceHistory(history=[(datetime.datetime.fromisoformat(x['datetime']), x['price']) for x in v])
        else:
            return PriceHistory(history=[])


class RetailerConfig(BaseModel):
    id: Optional[int] = None
    base_url: str
    scraping_method: str # valid options: ui, api, sitemap
    take_screenshots: bool = False
    selenium_settings: Dict[str, Any] = {
        'mode': 'uc',
        'headed': True,
        'proxy': None
    }


class RetailerSchema(BaseModel):
    id: Optional[int] = None
    name: str
    base_url: str
    scraping_config: RetailerConfig
    affiliate_tag: Optional[str] = None
    scrape_intervals: Dict[str, int] = {
        'current_year': 6 * 3600,    # 6 hours
        'previous_year': 12 * 3600,  # 12 hours
        'older': 24 * 3600          # 24 hours
    }
    excluded_brands: List[str] = []  # Default to empty list
    base_image_url: Optional[str] = None

    model_config = ConfigDict(coerce_numbers_to_str=True)


class ProductListingSchema(BaseModel):
    '''
    Schema for a product including its available prices.
    Does not include all fields of ProductSchema.
    '''
    id: int
    manufacturer_id: str
    name: str
    manufacturer: str
    category: Optional[str] = None
    base_image_url: Optional[str] = None
    description: Optional[str] = None
    release_year: Optional[int] = None
    prices: List[PriceSchema] = []