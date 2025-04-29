import sys
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple

project_root = str(Path(__file__).parent.parent)
sys.path.append(project_root)

from fastapi import FastAPI, Query # type: ignore
from fastapi.middleware.cors import CORSMiddleware # type: ignore
from shared.db.database import Database
from shared.schemas import ProductSchema, PriceSchema, ProductListingSchema
from shared.db.services.product_service import ProductService
from shared.db.services.price_service import PriceService
from shared.db.services.retailer_service import RetailerService


app = FastAPI()
db = Database()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000'],
    allow_credentials=True,
    allow_methods=['GET'],
    allow_headers=['Authorization', 'Content-Type']
)


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


# kann sein, dass wir das nicht mehr brauchen
@app.get('/manufacturers/{manufacturer}/products', response_model=List[ProductSchema])
async def get_products(
    manufacturer: str, 
    release_year: Optional[int] = None, 
    limit: Optional[int] = None,
    sort_by: Optional[str] = None,
    order: Optional[str] = 'desc'
):
    '''
    Returns a list of products for a given manufacturer with flexible filtering and sorting options.
    
    Parameters:
    - manufacturer: Name of the manufacturer
    - release_year: Optional year to filter products by
    - limit: Optional maximum number of products to return
    - sort_by: Optional field to sort by (e.g., 'release_year', 'name', 'price')
    - order: Optional sort order ('asc' or 'desc'), defaults to 'desc'
    '''
    with db.get_session() as session:
        product_service = ProductService(session)
        return product_service.get_by_manufacturer(
            manufacturer=manufacturer, 
            release_year=release_year, 
            limit=limit,
            sort_by=sort_by,
            order=order
        )
    

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
    

@app.get('/manufacturers/{manufacturer}/product_listings', response_model=Tuple[List[ProductListingSchema], int])
async def get_product_listings(
    manufacturer: str,
    release_year: List[int] = Query(default=[]),
    limit: int = 20,
    offset: int = 0
):
    '''
    Incrementally returns a list of ProductListingSchemas for a given manufacturer.
    Allows specifying a list of release years. Will only return products with at least one price in stock.
    '''
    with db.get_session() as session:
        product_service = ProductService(session)
        return product_service.get_available_products_by_manufacturer(
            manufacturer=manufacturer,
            release_year=release_year,
            limit=limit,
            offset=offset
        )