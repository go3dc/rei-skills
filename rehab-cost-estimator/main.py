import os
import ast
import logging
import pandas as pd
from utils.vision_analyzer import analyze_property_photos
from utils.cost_calculator import calculate_rehab_estimate

os.makedirs('logs', exist_ok=True)
logging.basicConfig(filename='logs/estimator.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def load_config():
    if not os.path.exists('config.py'):
        print("Config file missing. Using example configuration defaults...")
        import config_example as cfg
        return cfg
    import config as cfg
    return cfg

def load_input_leads():
    # Priority order: soft-filtered deals -> scraper leads
    paths = [
        '../buy-box-filter/processed_deals.csv',
        '../mls-deal-finder/scraped_leads.csv',
        '../mls-web-scraper/scraped_leads.csv'
    ]
    for path in paths:
        if os.path.exists(path):
            print(f"Loading property leads from: {path}")
            return pd.read_csv(path), path
            
    print("No upstream data sheets found.")
    custom_path = input("Enter path to listings CSV file: ").strip()
    return (pd.read_csv(custom_path), custom_path) if os.path.exists(custom_path) else (None, None)

def main():
    cfg = load_config()
    df_leads, source_path = load_input_leads()

    if df_leads is None or df_leads.empty:
        print("Execution halted: No records to process.")
        return

    print("\n================ REHAB COST ESTIMATOR RUNNING ================")
    updated_records = []
    
    for idx, row in df_leads.iterrows():
        lead = row.to_dict()
        address = lead.get('address', f'Property #{idx+1}')
        sqft = lead.get('sqft', 1500)
        
        # Extract photo URLs string or list
        raw_photos = lead.get('photo_urls', lead.get('image_urls', '[]'))
        try:
            photo_urls = ast.literal_eval(raw_photos) if isinstance(raw_photos, str) else raw_photos
        except Exception:
            photo_urls = []

        print(f"Analyzing visual assets for: {address}...")
        
        if photo_urls and cfg.VISION_API_KEY != "your_openai_api_key_here":
            assessment = analyze_property_photos(
                api_key=cfg.VISION_API_KEY,
                model_name=cfg.MODEL_NAME,
                image_urls=photo_urls,
                max_photos=cfg.MAX_PHOTOS_PER_LISTING
            )
        else:
            assessment = {"rehab_level": "medium", "notes": "No photo URLs found or API key default used."}

        estimated_repairs = calculate_rehab_estimate(assessment, sqft, cfg.COST_BENCHMARKS)
        
        lead['repairs'] = estimated_repairs
        lead['vision_rehab_level'] = assessment.get('rehab_level', 'medium')
        lead['vision_notes'] = assessment.get('notes', '')
        
        updated_records.append(lead)

    out_df = pd.DataFrame(updated_records)
    output_filename = "estimated_deals.csv"
    out_df.to_csv(output_filename, index=False)

    print("\n================ ANALYSIS COMPLETE ================")
    print(f"Processed Listings: {len(out_df)}")
    print(f"Updated Data Exported to: rehab-cost-estimator/{output_filename}")
    print("===================================================\n")

if __name__ == "__main__":
    main()
