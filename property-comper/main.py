import os
import logging
import pandas as pd
from utils.comp_finder import find_comps_with_ai
from utils.report_generator import generate_individual_reports

os.makedirs('logs', exist_ok=True)
logging.basicConfig(filename='logs/comper.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def load_config():
    if not os.path.exists('config.py'):
        print("Config file missing. Bootstrapping config.example.py settings...")
        import config_example as cfg
        return cfg
    import config as cfg
    return cfg

def load_input_leads():
    paths = [
        '../rehab-cost-estimator/estimated_deals.csv',
        '../buy-box-filter/processed_deals.csv',
        '../mls-deal-finder/scraped_leads.csv',
        '../mls-web-scraper/scraped_leads.csv'
    ]
    for path in paths:
        if os.path.exists(path):
            print(f"Loading property leads from: {path}")
            return pd.read_csv(path), path
            
    print("No upstream dataset found.")
    custom_path = input("Enter path to listings CSV file: ").strip()
    return (pd.read_csv(custom_path), custom_path) if os.path.exists(custom_path) else (None, None)

def main():
    cfg = load_config()
    df_leads, source_path = load_input_leads()

    if df_leads is None or df_leads.empty:
        print("Execution halted: No lead records available to comp.")
        return

    print("\n================ PROPERTY COMPER ENGINE RUNNING ================")
    updated_records = []

    for idx, row in df_leads.iterrows():
        lead = row.to_dict()
        address = lead.get('address', f'Property #{idx+1}')
        print(f"\n[{idx+1}/{len(df_leads)}] Finding comps & analyzing ARV for: {address}...")

        comp_result = find_comps_with_ai(lead, cfg)

        if comp_result:
            lead['arv'] = comp_result.estimated_arv
            lead['arv_summary'] = comp_result.valuation_summary
            
            generate_individual_reports(lead, comp_result, cfg)
            print(f"  ✓ Calculated ARV: ${int(comp_result.estimated_arv):,}")
            print(f"  ✓ Reports saved to {cfg.REPORTS_DIR}/comps_{address.replace(' ', '_').lower()[:15]}*")
        else:
            print(f"  ❌ Failed to generate comps for {address}. Retaining default ARV.")

        updated_records.append(lead)

    out_df = pd.DataFrame(updated_records)
    output_filename = "comped_deals.csv"
    out_df.to_csv(output_filename, index=False)

    print("\n================ COMP ANALYSIS COMPLETE ================")
    print(f"Total Properties Evaluated: {len(out_df)}")
    print(f"Master Dataset Exported to: property-comper/{output_filename}")
    print(f"Individual Project Reports: {cfg.REPORTS_DIR}/")
    print("========================================================\n")

if __name__ == "__main__":
    main()
