import logging
import os
from utils.normalizer import normalize_address
from utils.state_manager import StateManager
from utils.metrics import log_run_stats

os.makedirs('logs', exist_ok=True)
logging.basicConfig(filename='logs/scraper.log', level=logging.INFO)

def run_scraper(zip_codes):
    state = StateManager()
    metrics = {"found": 0, "errors": 0}
    for zip_code in zip_codes:
        if state.is_processed(zip_code): continue
        try:
            logging.info(f"Scraping: {zip_code}")
            metrics["found"] += 1
            state.mark_as_processed(zip_code)
        except Exception as e:
            logging.error(f"Error in {zip_code}: {e}")
            metrics["errors"] += 1
    log_run_stats(metrics["found"], metrics["errors"])

if __name__ == "__main__":
    run_scraper(["90210", "10001"])
