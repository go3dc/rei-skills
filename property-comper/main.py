import pandas as pd
import os
import json
from utils.geo import calculate_distance
from utils.valuation import filter_comps, calculate_arv

def run_valuation():
    # Load target property configurations
    if not os.path.exists('target_property.json'):
        print("Error: target_property.json not found. Please create it first.")
        return
        
    with open('target_property.json', 'r') as f:
        subject = json.load(f)
        
    if not os.path.exists('historical_solds.csv'):
        print("Error: historical_solds.csv not found. Please provide recent sold market data.")
        return
        
    # Load the pool of recently sold homes
    df = pd.read_csv('historical_solds.csv')
    
    # Step 1: Calculate distance from subject property for every sold home
    df['distance_miles'] = df.apply(
        lambda row: calculate_distance(subject['latitude'], subject['longitude'], row['latitude'], row['longitude']), 
        axis=1
    )
    
    # Step 2: Filter down to true comparable properties
    comps_df = filter_comps(df, subject)
    
    # Step 3: Run the numbers
    valuation_report = calculate_arv(comps_df, subject)
    
    # Save results
    with open('valuation_report.json', 'w') as f:
        json.dump(valuation_report, f, indent=4)
        
    print(f"Valuation Complete! Estimated ARV: ${valuation_report['estimated_arv']:,}")

if __name__ == "__main__":
    run_valuation()
