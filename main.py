import time
import random
import logging
from utils.normalizer import normalize_address
from utils.state_manager import StateManager
from utils.metrics import log_run_stats

# Setup logging
logging.basicConfig(filename='logs/scraper.log', level=logging.INFO)

def run_scraper(zip_codes):
    state = StateManager()
    start_time = time.time()
    listings_found = 0
    
    for zip_code in zip_codes:
        if state.is_processed(zip_code):
            continue
            
        logging.info(f"Scraping zip code: {zip_code}")
        # Add your scraping logic here
        time.sleep(random.uniform(5, 15)) 
        
        state.mark_as_processed(zip_code)
        listings_found += 1
        
    duration = time.time() - start_time
    log_run_stats(listings_found, duration)

if __name__ == "__main__":
    run_scraper(["90210", "10001"])
