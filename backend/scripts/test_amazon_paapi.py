import os
from amazon_paapi import AmazonApi
from dotenv import load_dotenv
import traceback

# Load credentials from .env
load_dotenv()

ACCESS_KEY = os.getenv('PA_API_ACCESS_KEY')
SECRET_KEY = os.getenv('PA_API_SECRET_KEY')
ASSOCIATE_TAG = os.getenv('PA_API_ASSOCIATE_TAG', 'dekobricks-21')  # Replace with your tag or set in .env
REGION = os.getenv('PA_API_REGION', 'DE')  # Default to Germany

if not ACCESS_KEY or not SECRET_KEY:
    print('Missing PA_API_ACCESS_KEY or PA_API_SECRET_KEY in .env')
    exit(1)

# Initialize API client
amazon = AmazonApi(ACCESS_KEY, SECRET_KEY, ASSOCIATE_TAG, REGION)

# Example: Search for "lego"
try:
    result = amazon.search_items(keywords="lego", search_index="All", item_count=1)
    print(result)
except Exception as e:
    print(f"Error: {e}")
    traceback.print_exc()
    if hasattr(e, 'response'):
        print('Response status code:', getattr(e.response, 'status_code', None))
        print('Response content:', getattr(e.response, 'content', None)) 