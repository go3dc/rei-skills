import json
import os
import pandas as pd
from utils.matcher import matches_buy_box

def load_buy_box():
    config_file = 'buy_box.json' if os.path.exists('buy_box.json') else 'buy_box.example.json'
    with open(config_file, 'r') as f:
        return json.load(f)

def get_property_leads():
    print("\n--- Buy Box Filter Intake System ---")
    print("1) Load automatically from scraper-v1 MLS output data sheet")
    print("2) Import custom external off-market CSV file list")
    print("3) Manually transcribe single deal characteristics")
    choice = input("Select property source execution method (1-3): ").strip()

    if choice == '1':
        path = '../scraper-v1/scraped_leads.csv'
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

    qualified = []
    for lead in leads:
        passed, _ = matches_buy_box(lead, buy_box)
        if passed:
            # Safely bind missing keys to prevent pipeline execution breaks
            if 'lot_size' not in lead:
                lead['lot_size'] = None
            qualified.append(lead)

    print(f"\nFiltering complete. Identified {len(qualified)} matching targets.")
    if qualified:
        pd.DataFrame(qualified).to_csv('qualified_deals.csv', index=False)
        print("Exported matching assets directly to: buy-box-filter/qualified_deals.csv")

if __name__ == "__main__":
    main()
