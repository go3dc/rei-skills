import os
import json
import logging
import pandas as pd
from utils.api_handler import fetch_mls_data
from utils.normalizer import normalize_api_data

# Setting up structural operations metrics directory
os.makedirs('logs', exist_ok=True)
logging.basicConfig(filename='logs/api.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

def load_config():
    if not os.path.exists('config.py'):
        print("Config file not found. Falling back to config.example.py settings...")
        import config_example as cfg
        return cfg
    import config as cfg
    return cfg

def main():
    cfg = load_config()
    
    if not hasattr(cfg, 'APIFY_TOKEN') or cfg.APIFY_TOKEN == "your_apify_api_token_here":
        print("Error: A valid APIFY_TOKEN is required inside config.py to execute calculations.")
        return

    print(f"Initializing MLS Deal Finder API Client...")
    
    # Step 1: Query API to pull real-time raw inventory datasets
    raw_data = fetch_mls_data(
        token=cfg.APIFY_TOKEN,
        actor_id=cfg.ACTOR_ID,
        locations=cfg.TARGET_LOCATIONS,
        max_items=cfg.MAX_ITEMS_PER_LOCATION
    )
    
    if not raw_data:
        print("No raw real estate data retrieved from the endpoint. Halting engine.")
        return

    # Step 2: Extract nested arrays into uniform target row blocks
    print(f"Normalizing API payloads into uniform pipeline templates...")
    normalized_leads = normalize_api_data(raw_data)

    # Step 3: Export the structured dataframe out to the shared ecosystem file
    df = pd.DataFrame(normalized_leads)
    output_filename = "scraped_leads.csv"
    df.to_csv(output_filename, index=False)
    
    print(f"\n================ ENGINE EXECUTION COMPLETE ================")
    print(f"Total Raw API Elements Analyzed: {len(raw_data)}")
    print(f"Successfully Normalized & Saved: {len(df)} leads")
    print(f"Target Output Path destination: mls-deal-finder/{output_filename}")
    print(f"===========================================================")

if __name__ == "__main__":
    main()
