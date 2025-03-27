import logging
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
import json
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NextloadScraper:
    def __init__(self):
        """Initialize the NextLoad scraper with Chrome in headless mode"""
        self.base_url = "https://www.nextload.com"
        self.search_url = f"{self.base_url}/loads/search"
        self.setup_driver()
        
    def setup_driver(self):
        """Set up the Chrome WebDriver with appropriate options"""
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        
        # Use a built-in Chrome binary instead of installing via ChromeDriverManager
        # since we're in a replit environment
        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            logger.info("Chrome WebDriver initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Chrome WebDriver: {e}")
            # Fallback to using ChromeDriverManager
            try:
                service = Service(ChromeDriverManager().install())
                self.driver = webdriver.Chrome(service=service, options=chrome_options)
                logger.info("Chrome WebDriver initialized with ChromeDriverManager")
            except Exception as e:
                logger.error(f"Failed to initialize Chrome WebDriver with ChromeDriverManager: {e}")
                raise

    def close(self):
        """Close the WebDriver"""
        if hasattr(self, 'driver'):
            self.driver.quit()
            logger.info("WebDriver closed")

    def search_loads(self, origin_state=None, destination_state=None, equipment_type=None):
        """
        Search for loads on Nextload.com based on criteria
        
        Args:
            origin_state: State abbreviation for origin (e.g., 'CA')
            destination_state: State abbreviation for destination (e.g., 'TX')
            equipment_type: Type of equipment needed (e.g., 'Flatbed', 'Reefer')
            
        Returns:
            List of load data dictionaries
        """
        try:
            logger.info(f"Searching for loads: origin={origin_state}, destination={destination_state}, equipment={equipment_type}")
            
            # Navigate to the search page
            self.driver.get(self.search_url)
            time.sleep(3)  # Allow page to load
            
            # If we need to input search criteria, we would do it here
            # For now, we'll just scrape what's visible on the page
            
            # Extract load data
            load_data = self._extract_load_data()
            return load_data
            
        except Exception as e:
            logger.error(f"Error during load search: {e}")
            return []

    def _extract_load_data(self):
        """Extract load data from the search results page"""
        loads = []
        try:
            # Wait for the load cards to appear
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "load-card"))
            )
            
            # Find all load cards
            load_cards = self.driver.find_elements(By.CLASS_NAME, "load-card")
            logger.info(f"Found {len(load_cards)} load cards")
            
            for card in load_cards:
                try:
                    # Extract data from each card
                    load = {}
                    
                    # Get route information
                    route_info = card.find_element(By.CLASS_NAME, "route-info").text
                    route_parts = route_info.split(" to ")
                    if len(route_parts) >= 2:
                        load["origin"] = route_parts[0].strip()
                        load["destination"] = route_parts[1].strip()
                    
                    # Get price information if available
                    try:
                        price_elem = card.find_element(By.CLASS_NAME, "price")
                        load["price"] = price_elem.text.strip()
                    except NoSuchElementException:
                        load["price"] = "Not specified"
                    
                    # Get distance information if available
                    try:
                        distance_elem = card.find_element(By.CLASS_NAME, "distance")
                        load["distance"] = distance_elem.text.strip()
                    except NoSuchElementException:
                        load["distance"] = "Not specified"
                    
                    # Get equipment type if available
                    try:
                        equipment_elem = card.find_element(By.CLASS_NAME, "equipment-type")
                        load["equipment_type"] = equipment_elem.text.strip()
                    except NoSuchElementException:
                        load["equipment_type"] = "Not specified"
                    
                    # Add timestamp
                    load["scraped_at"] = datetime.now().isoformat()
                    
                    loads.append(load)
                except Exception as e:
                    logger.error(f"Error extracting data from load card: {e}")
                    continue
                    
        except TimeoutException:
            logger.error("Timeout waiting for load cards to appear")
        except Exception as e:
            logger.error(f"Error extracting load data: {e}")
            
        return loads

    def get_load_details(self, load_id):
        """
        Get detailed information about a specific load
        
        Args:
            load_id: The ID of the load to retrieve details for
            
        Returns:
            Dictionary with load details
        """
        try:
            detail_url = f"{self.base_url}/loads/{load_id}"
            self.driver.get(detail_url)
            
            # Wait for details to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "load-details"))
            )
            
            # Extract detailed information
            details = {}
            
            # This is a placeholder for actual detail extraction
            # You would need to inspect the actual page structure to extract real data
            details["id"] = load_id
            details["status"] = "Available"
            
            return details
            
        except Exception as e:
            logger.error(f"Error getting load details for {load_id}: {e}")
            return None

# Example usage
if __name__ == "__main__":
    scraper = NextloadScraper()
    try:
        loads = scraper.search_loads(origin_state="CA", destination_state="TX")
        print(json.dumps(loads, indent=2))
    finally:
        scraper.close()