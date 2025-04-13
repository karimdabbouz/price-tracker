import sys
from pathlib import Path
from typing import List, Dict, Any, Optional

project_root = str(Path(__file__).parent.parent)
sys.path.append(project_root)

from fastapi import FastAPI
from shared.db.database import Database
from shared.schemas import ProductSchema, PriceSchema, RetailerSchema
from shared.db.services.product_service import ProductService
from shared.db.services.price_service import PriceService
from shared.db.services.retailer_service import RetailerService


app = FastAPI()
db = Database()


@app.get('/')
def read_root():
    return {'lorem': 'ipsum'}


@app.get('/manufacturers', response_model=List[Dict[str, Any]])
async def get_manufacturers():
    '''
    Returns a list of manufacturer names and their ID.
    '''
    with db.get_session() as session:
        retailer_service = RetailerService(session)
        retailer_list = retailer_service.get_all()
        print(retailer_list[0].model_dump())
        return [
            {
                'id': retailer.id,
                'name': retailer.name
            }
            for retailer in retailer_list
        ]


@app.get('/manufacturers/{manufacturer}/products', response_model=List[ProductSchema])
async def get_products(manufacturer: str, release_year: Optional[int] = None, limit: Optional[int] = None):
    '''
    Returns a list of products for a given manufacturer with filtering options for release year and limit.
    '''
    with db.get_session() as session:
        product_service = ProductService(session)
        return product_service.get_by_manufacturer(manufacturer=manufacturer, release_year=release_year, limit=limit)
    

@app.get('/products/autocomplete', response_model=List[Dict[str, Any]])
async def get_product_autocomplete():
    '''
    Gets ID and name for all products for the autocomplete search.
    '''
    with db.get_session() as session:
        product_service = ProductService(session)
        return product_service.get_autocomplete()


@app.get('/products/{id}', response_model=ProductSchema)
async def get_product(id: int):
    '''
    Returns a product by its ID.
    '''
    with db.get_session() as session:
        product_service = ProductService(session)
        return product_service.get_by_id(id)
    

@app.get('/products/{product_id}/prices', response_model=List[PriceSchema])
async def get_product_prices(product_id: int):
    '''
    Returns a list of prices for a given product.
    '''
    with db.get_session() as session:
        price_service = PriceService(session)
        return price_service.get_by_product_id(product_id)