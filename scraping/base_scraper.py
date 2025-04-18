from abc import ABC, abstractmethod
from typing import List, Dict, Any
from seleniumbase import Driver
from shared.db.models import Product
from shared.schemas import ProductSchema, PriceSchema, RetailerConfig
from shared.logger import logger
import os, datetime


class BaseScraper(ABC):
    def __init__(self, retailer_config: RetailerConfig):
        self.retailer_config = retailer_config
        self.scraping_mode = retailer_config.scraping_method
        self.selenium_settings = retailer_config.selenium_settings
    

    def _initialize_driver(self) -> Driver:
        if self.scraping_mode == 'ui':
            if self.selenium_settings['mode'] == 'uc':
                try:
                    driver = Driver(uc=True, headless=not self.selenium_settings['headed'], proxy=self.selenium_settings['proxy'])
                    driver.set_window_size(1920, 1080)
                    return driver
                except Exception as e:
                    raise Exception(f'Error initializing driver: {e}')
            else:
                try:
                    driver = Driver(wire=True, headless=self.selenium_settings['headed'], proxy=self.selenium_settings['proxy'])
                    driver.set_window_size(1920, 1080)
                    return driver
                except Exception as e:
                    raise Exception(f'Error initializing driver: {e}')
        elif self.scraping_mode == 'api':
            logger.info('Note: Using a proxy will probably interfere with capturing API requests. Use UI or SITEMAP mode instead.')
            if self.selenium_settings['mode'] == 'uc':
                raise Exception('UC mode is not supported for API scraping. Use UI or SITEMAP mode instead.')
            else:
                try:
                    driver = Driver(wire=True, headless=self.selenium_settings['headed'], proxy=self.selenium_settings['proxy'])
                    driver.set_window_size(1920, 1080)
                    return driver
                except Exception as e:
                    raise Exception(f'Error initializing driver: {e}')
        elif self.scraping_mode == 'sitemap':
            if self.selenium_settings['mode'] == 'uc':
                try:
                    driver = Driver(uc=True, headless=not self.selenium_settings['headed'], proxy=self.selenium_settings['proxy'])
                    driver.set_window_size(1920, 1080)
                    return driver
                except Exception as e:
                    raise Exception(f'Error initializing driver: {e}')
            else:
                try:
                    driver = Driver(wire=True, headless=self.selenium_settings['headed'], proxy=self.selenium_settings['proxy'])
                    driver.set_window_size(1920, 1080)
                    return driver
                except Exception as e:
                    raise Exception(f'Error initializing driver: {e}')
        else:
            raise ValueError(f'Invalid value for scraping_method: {e}')


    def _take_screenshot(self, driver: Driver):
        '''
        Takes a screenshot of the current page and saves it to the screenshots directory.
        '''
        screenshots_dir = '/app/screenshots'
        if not os.path.exists(screenshots_dir):
            os.makedirs(screenshots_dir)
        
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        screenshot_path = os.path.join(screenshots_dir, f'screenshot_{timestamp}.png')
        driver.save_screenshot(screenshot_path)


    @abstractmethod
    def scrape_product_ui(self, driver: Driver, product: ProductSchema) -> List[Dict[str, Any]]:
        '''
        Uses the UI to search for a product. Opens the product page.
        
        Args:
            product: ProductSchema containing data to use in search.
        '''
        pass


    @abstractmethod
    def scrape_product_api(self):
        '''
        Implement later
        '''
        pass


    @abstractmethod
    def scrape_product_sitemap(self):
        '''
        Implement later
        '''
        pass

    
    @abstractmethod
    def _parse_price_schema(self, product: Product, data: Dict[str, Any]) -> PriceSchema:
        '''
        Parses the data into a PriceSchema
        '''
        pass


    def run(self, products: List[ProductSchema]) -> List[PriceSchema]:
        '''
        Scrapes prices for a list of products for the retailer defined in retailer_config.

        Args:
            products: List of ProductSchema instances to scrape
            
        Returns:
            List of PriceSchema objects containing the scraped price data
        '''
        if self.scraping_mode == 'ui':
            driver = self._initialize_driver()
            results = []
            try:
                for product in products:
                    try:
                        result = self.scrape_product_ui(driver, product)
                        if result:
                            results.append(result)
                    except Exception as e:
                        logger.error(f'Error scraping product {product.manufacturer_id}: {str(e)}')
                        continue
                return results
            finally:
                driver.quit()
        elif self.scraping_mode == 'api':
            pass
            # implement later
        elif self.scraping_mode == 'sitemap':
            pass
            # implement later