import json
import os
import pandas as pd
from utils.matcher import matches_buy_box

def load_buy_box():
    config_file = 'buy_box.json' if os.path.exists('buy_box.json') else 'buy_box.example.json'
    with open(config_file, 'r') as f:
        return json.load(f)

def get_property_leads():
    print("\n--- Buy Box Soft-Filter Intake System ---")
    print("1) Load automatically from mls-web-scraper output")
    print("2) Import custom external off-market CSV file list")
    print("3) Manually transcribe single deal characteristics")
    choice = input("Select property source execution method (1-3): ").strip()

    if choice == '1':
        path = '../mls-web-scraper/scraped_leads.csv'
        if not os.path.exists(path):
            path = input("File not found. Paste path to your scraped data CSV: ").strip()
        return pd.read_csv(path).to_dict(orient='records') if os.path.exists(path) else None

    elif choice == '2':
        path = input("Enter path to custom lead spreadsheet: ").strip()
        return pd.read_csv(path).to_dict(orient='records') if os.path.exists(path) else None

    elif choice == '3':
        return [{
            "address": input("Street Address: "),
            "zip_code": input("Zip Code: "),
            "price": int(input("Price ($): ") or 0),
            "beds": int(input("Bedrooms count: ") or 0),
            "baths": float(input("Bathrooms count: ") or 0),
            "sqft": int(input("Interior Living Square Feet: ") or 0),
            "lot_size": float(input("Lot Size in Acres (Enter to skip): ") or 0.0),
            "year_built": int(input("Year Built (Enter to skip): ") or 0),
            "property_type": input("Property Classification: ")
        }]
    return None

def main():
    buy_box = load_buy_box()
    leads = get_property_leads()
    
    if not leads:
        print("Execution halted: Empty lead queue matrix.")
        return

    processed_leads = []
    passed_count = 0
    failed_count = 0

    for lead in leads:
        passed, reason = matches_buy_box(lead, buy_box)
        
        # Soft Filter: Label instead of discarding
        lead['in_buy_box'] = passed
        lead['buy_box_fail_reason'] = "" if passed else reason
        
        # Safely bind missing keys to prevent downstream pipeline breaks
        if 'lot_size' not in lead or pd.isna(lead.get('lot_size')):
            lead['lot_size'] = None
            
        if passed:
            passed_count += 1
        else:
            failed_count += 1
            
        processed_leads.append(lead)

    print(f"\nProcessing complete. Total leads: {len(processed_leads)}")
    print(f"✅ In Buy Box: {passed_count}")
    print(f"❌ Out of Buy Box: {failed_count}")
    
    if processed_leads:
        pd.DataFrame(processed_leads).to_csv('processed_deals.csv', index=False)
        print("Saved all evaluated assets directly to: buy-box-filter/processed_deals.csv")

if __name__ == "__main__":
    main()
