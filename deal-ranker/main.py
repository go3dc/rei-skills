import json
import os
import pandas as pd
from utils.scoring import evaluate_deal_metrics

def load_config():
    config_file = 'ranker_config.json' if os.path.exists('ranker_config.json') else 'ranker_config.example.json'
    with open(config_file, 'r') as f:
        return json.load(f)

def load_source_leads():
    # Attempting to load from soft-filter processed output first
    path = '../buy-box-filter/processed_deals.csv'
    if not os.path.exists(path):
        # Fallback 1: Check old qualified_deals path
        path = '../buy-box-filter/qualified_deals.csv'
    if not os.path.exists(path):
        # Fallback 2: Check raw web scraper output directly
        path = '../mls-web-scraper/scraped_leads.csv'
        
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

    # Dynamic columns integration for properties missing explicit valuation inputs
    if 'arv' not in df_leads.columns:
        df_leads['arv'] = df_leads['price']
    if 'repairs' not in df_leads.columns:
        df_leads['repairs'] = 0
    if 'lot_size' not in df_leads.columns:
        df_leads['lot_size'] = None
        
    # Safeguard: If leads are loaded directly bypassing the buy-box step, default them to 'in the buy box'
    if 'in_buy_box' not in df_leads.columns:
        df_leads['in_buy_box'] = True
    if 'buy_box_fail_reason' not in df_leads.columns:
        df_leads['buy_box_fail_reason'] = ""

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
    
    # Sorting sequence: Priority Tier (Tier 1 is best, Tier 4 is worst), then Score (Descending), then Gap (Ascending)
    out_df.sort_values(
        by=['priority_tier', 'deal_score', 'financial_gap'], 
        ascending=[True, False, True], 
        inplace=True
    )

    out_df.to_csv('pipeline_ranked_deals.csv', index=False)
    
    # Generate terminal analysis metrics
    t1_count = len(out_df[out_df['priority_tier'] == 1])
    t2_count = len(out_df[out_df['priority_tier'] == 2])
    t3_count = len(out_df[out_df['priority_tier'] == 3])
    t4_count = len(out_df[out_df['priority_tier'] == 4])
    
    print(f"\n================ PIPELINE RANKING ANALYSIS RESULT ================")
    print(f"Total Listings Processed: {len(out_df)}")
    print(f"🚨 Tier 1 (Home Runs):       {t1_count}")
    print(f"📈 Tier 2 (Negotiable):      {t2_count}")
    print(f"🔍 Tier 3 (Wide Price Gap):  {t3_count}")
    print(f"⚠️  Tier 4 (Out of Buy Box):  {t4_count}")
    print(f"==================================================================")
    
    # Show top 5 properties in pipeline
    print("\n>>> PIPELINE PRIORITY PREVIEW (Top 5 Ranked Deals):")
    for idx, row in out_df.head(5).iterrows():
        tier_label = f"Tier {int(row['priority_tier'])}"
        if row['priority_tier'] == 4:
            tier_label += " (Out of Buy Box)"
        print(f" - [{tier_label}] {row['address']} | Price: ${int(row['price']):,} | Score: {row['deal_score']} | Fail Reason: {row.get('buy_box_fail_reason', '')}")
        
    print("\nComplete optimization ledger saved to: deal-ranker/pipeline_ranked_deals.csv")

if __name__ == "__main__":
    main()
