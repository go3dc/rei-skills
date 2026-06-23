import json
import os
import pandas as pd
from utils.matcher import matches_buy_box

def load_buy_box():
    config_file = 'buy_box.json' if os.path.exists('buy_box.json') else 'buy_box.example.json'
    with open(config_file, 'r') as f:
        return json.load(f)

def get_property_leads():
    print("\n--- REI Buy Box Lead Source Selector ---")
    print("1) Load from scraper-v1 output (Default MLS Scraper)")
    print("2) Load from an external/custom CSV file")
    print("3) Manually type in a single property's specs")
    choice = input("Select an input source option (1-3): ").strip()

    if choice == '1':
        # Direct relative path fallback to look into your sibling folder layout
        path = '../scraper-v1/scraped_leads.csv'
        if not os.path.exists(path):
            path = input("Couldn't find default file. Please paste the path to your scraper CSV: ").strip()
        return pd.read_csv(path).to_dict(orient='records') if os.path.exists(path) else None

    elif choice == '2':
        path = input("Enter the full path to your custom CSV file: ").strip()
        return pd.read_csv(path).to_dict(orient='records') if os.path.exists(path) else None

    elif choice == '3':
        print("\nEnter property specs manually:")
        return [{
            "address": input("Address: "),
            "zip_code": input("Zip Code: "),
            "price": int(input("Price (numbers only): ") or 0),
            "beds": int(input("Beds: ") or 0),
            "baths": float(input("Baths: ") or 0),
            "sqft": int(input("SqFt: ") or 0),
            "year_built": int(input("Year Built (Enter to skip): ") or 0),
            "property_type": input("Property Type (e.g., Single Family): ")
        }]
    return None

def main():
    buy_box = load_buy_box()
    leads = get_property_leads()
    
    if not leads:
        print("No leads loaded. Closing script.")
        return

    qualified = []
    disqualified_count = 0

    for lead in leads:
        passed, reason = matches_buy_box(lead, buy_box)
        if passed:
            qualified.append(lead)
        else:
            disqualified_count += 1

    # Output Results
    print(f"\n--- Processing Complete ---")
    print(f"Total Evaluated: {len(leads)}")
    print(f"✅ Qualified: {len(qualified)}")
    print(f"❌ Disqualified: {disqualified_count}")

    if qualified:
        out_df = pd.DataFrame(qualified)
        out_df.to_csv('qualified_deals.csv', index=False)
        print("Saved matching leads to: buy-box-filter/qualified_deals.csv")

if __name__ == "__main__":
    main()
