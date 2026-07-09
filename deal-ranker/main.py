import json
import os
import pandas as pd
from utils.scoring import evaluate_deal_metrics

def load_config():
    config_file = 'ranker_config.json' if os.path.exists('ranker_config.json') else 'ranker_config.example.json'
    with open(config_file, 'r') as f:
        return json.load(f)

def load_source_leads():
    path = '../buy-box-filter/qualified_deals.csv'
    if not os.path.exists(path):
        path = '../scraper-v1/scraped_leads.csv'
    if not os.path.exists(path):
        print(f"Data stream file unavailable.")
        path = input("Provide path to clean listings CSV: ").strip()
    return pd.read_csv(path) if os.path.exists(path) else None

def main():
    config = load_config()
    df_leads = load_source_leads()
    
    if df_leads is None or df_leads.empty:
        print("Processing terminated: Empty data sheet.")
        return

    # Synchronize default headers to match updated buy box schemas
    if 'arv' not in df_leads.columns:
        df_leads['arv'] = df_leads['price']
    if 'repairs' not in df_leads.columns:
        df_leads['repairs'] = 0
    if 'lot_size' not in df_leads.columns:
        df_leads['lot_size'] = None

    records = df_leads.to_dict(orient='records')
    processed_output = []

    for item in records:
        tier, score, gap, mao = evaluate_deal_metrics(item, config)
        item['calculated_mao'] = mao
        item['financial_gap'] = gap
        item['deal_score'] = score
        item['priority_tier'] = tier
        processed_output.append(item)

    out_df = pd.DataFrame(processed_output)
    out_df.sort_values(
        by=['priority_tier', 'deal_score', 'financial_gap'], 
        ascending=[True, False, True], 
        inplace=True
    )

    out_df.to_csv('pipeline_ranked_deals.csv', index=False)
    print(f"\nPipeline Analysis Completed. Output compiled inside deal-ranker/pipeline_ranked_deals.csv.")

if __name__ == "__main__":
    main()
