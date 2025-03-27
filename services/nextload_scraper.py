import logging
import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementNotInteractableException
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
        self.login_url = f"{self.base_url}/login"
        self.search_url = f"{self.base_url}/loads/search"
        self.email = "visql7@gmail.com"
        self.password = "fleettrackpro"
        self.is_logged_in = False
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
                
    def login(self):
        """Login to nextload.com with the provided credentials"""
        if self.is_logged_in:
            logger.info("Already logged in to NextLoad")
            return True
            
        try:
            logger.info("Attempting to log in to NextLoad...")
            self.driver.get(self.login_url)
            time.sleep(3)  # Allow page to load
            
            # Find the email and password fields and enter credentials
            try:
                email_field = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.ID, "email"))
                )
                email_field.clear()
                email_field.send_keys(self.email)
                
                password_field = self.driver.find_element(By.ID, "password")
                password_field.clear()
                password_field.send_keys(self.password)
                
                # Click the login button
                login_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
                login_button.click()
                
                # Wait for login to complete
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "dashboard"))
                )
                
                logger.info("Successfully logged in to NextLoad")
                self.is_logged_in = True
                return True
                
            except (NoSuchElementException, TimeoutException) as e:
                logger.error(f"Login form elements not found: {e}")
                # Try alternative login form if exists
                try:
                    email_field = WebDriverWait(self.driver, 5).until(
                        EC.presence_of_element_located((By.NAME, "email"))
                    )
                    email_field.clear()
                    email_field.send_keys(self.email)
                    
                    password_field = self.driver.find_element(By.NAME, "password")
                    password_field.clear()
                    password_field.send_keys(self.password)
                    
                    # Find login button by various methods
                    try:
                        login_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Login')]")
                    except NoSuchElementException:
                        try:
                            login_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Sign In')]")
                        except NoSuchElementException:
                            login_button = self.driver.find_element(By.CSS_SELECTOR, "form button[type='submit']")
                    
                    login_button.click()
                    
                    # Wait for redirect after login
                    time.sleep(5)
                    
                    # Check if login was successful
                    if "/dashboard" in self.driver.current_url or "/loads" in self.driver.current_url:
                        logger.info("Successfully logged in to NextLoad using alternative method")
                        self.is_logged_in = True
                        return True
                    else:
                        logger.warning("Login potentially failed. Current URL: " + self.driver.current_url)
                        return False
                        
                except Exception as e2:
                    logger.error(f"Alternative login attempt failed: {e2}")
                    return False
                
        except Exception as e:
            logger.error(f"Error during login: {e}")
            return False

    def close(self):
        """Close the WebDriver"""
        if hasattr(self, 'driver'):
            self.driver.quit()
            logger.info("WebDriver closed")

    def search_loads(self, origin_state=None, destination_state=None, equipment_type=None):
        """
        Search for loads on Nextload.com based on criteria
        
        Args:
            origin_state: State name or abbreviation for origin (e.g., 'California' or 'CA')
            destination_state: State name or abbreviation for destination (e.g., 'Texas' or 'TX')
            equipment_type: Type of equipment needed (e.g., 'Flatbed', 'Reefer')
            
        Returns:
            List of load data dictionaries
        """
        try:
            logger.info(f"Searching for loads: origin={origin_state}, destination={destination_state}, equipment={equipment_type}")
            
            # Ensure we're logged in
            if not self.is_logged_in and not self.login():
                logger.error("Failed to log in to NextLoad. Cannot search for loads.")
                return []
            
            # Navigate to the search page
            self.driver.get(self.search_url)
            time.sleep(3)  # Allow page to load
            
            # Try to apply search filters if provided
            if origin_state or destination_state or equipment_type:
                try:
                    # Find and click on "Advanced Search" or filter button if available
                    try:
                        advanced_search_btn = WebDriverWait(self.driver, 5).until(
                            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Advanced Search')]"))
                        )
                        advanced_search_btn.click()
                        time.sleep(1)
                    except (TimeoutException, NoSuchElementException):
                        # Try looking for filter button
                        try:
                            filter_btn = WebDriverWait(self.driver, 3).until(
                                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Filter')]"))
                            )
                            filter_btn.click()
                            time.sleep(1)
                        except (TimeoutException, NoSuchElementException):
                            logger.warning("Could not find advanced search or filter buttons")
                    
                    # Apply origin state filter if provided
                    if origin_state:
                        try:
                            origin_input = WebDriverWait(self.driver, 5).until(
                                EC.presence_of_element_located((By.ID, "origin-state"))
                            )
                            origin_input.clear()
                            origin_input.send_keys(origin_state)
                            origin_input.send_keys(Keys.TAB)
                            time.sleep(1)
                        except (TimeoutException, NoSuchElementException, ElementNotInteractableException):
                            logger.warning(f"Could not set origin state filter: {origin_state}")
                    
                    # Apply destination state filter if provided
                    if destination_state:
                        try:
                            dest_input = WebDriverWait(self.driver, 5).until(
                                EC.presence_of_element_located((By.ID, "destination-state"))
                            )
                            dest_input.clear()
                            dest_input.send_keys(destination_state)
                            dest_input.send_keys(Keys.TAB)
                            time.sleep(1)
                        except (TimeoutException, NoSuchElementException, ElementNotInteractableException):
                            logger.warning(f"Could not set destination state filter: {destination_state}")
                    
                    # Apply equipment type filter if provided
                    if equipment_type:
                        try:
                            equip_input = WebDriverWait(self.driver, 5).until(
                                EC.presence_of_element_located((By.ID, "equipment-type"))
                            )
                            equip_input.clear()
                            equip_input.send_keys(equipment_type)
                            equip_input.send_keys(Keys.TAB)
                            time.sleep(1)
                        except (TimeoutException, NoSuchElementException, ElementNotInteractableException):
                            logger.warning(f"Could not set equipment type filter: {equipment_type}")
                    
                    # Apply filters by clicking search button
                    try:
                        search_btn = WebDriverWait(self.driver, 5).until(
                            EC.element_to_be_clickable((By.XPATH, "//button[@type='submit' or contains(text(), 'Search')]"))
                        )
                        search_btn.click()
                        time.sleep(3)  # Wait for results to load
                    except (TimeoutException, NoSuchElementException):
                        logger.warning("Could not find search button to apply filters")
                        
                except Exception as filter_err:
                    logger.error(f"Error applying search filters: {filter_err}")
                    # Continue with unfiltered results
            
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