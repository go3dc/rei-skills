import pandas as pd

def filter_comps(df, subject):
    """
    Filters historical data to properties within 0.5 miles, 
    +/- 20% square footage, and matching bed/bath ranges.
    """
    # Rule 1: Proximity check (Within 0.5 miles)
    mask = df['distance_miles'] <= 0.5
    
    # Rule 2: Size check (+/- 20% of subject square footage)
    min_sqft = subject['sqft'] * 0.8
    max_sqft = subject['sqft'] * 1.2
    mask &= (df['sqft'] >= min_sqft) & (df['sqft'] <= max_sqft)
    
    # Rule 3: Layout check (+/- 1 bedroom/bathroom)
    mask &= (df['beds'] >= subject['beds'] - 1) & (df['beds'] <= subject['beds'] + 1)
    
    filtered_df = df[mask].copy()
    
    # Sort by closest proximity and return top 5 best matches
    return filtered_df.sort_values(by='distance_miles').head(5)

def calculate_arv(comps_df, subject):
    if comps_df.empty:
        return {"error": "No comparable sales found within parameters."}
        
    # Calculate price per square foot for each comp
    comps_df['price_per_sqft'] = comps_df['price'] / comps_df['sqft']
    
    avg_price_per_sqft = comps_df['price_per_sqft'].mean()
    estimated_arv = round(subject['sqft'] * avg_price_per_sqft)
    
    # Prepare details of comps used
    comps_used = comps_df[['address', 'price', 'sqft', 'distance_miles']].to_dict(orient='records')
    
    return {
        "subject_address": subject['address'],
        "estimated_arv": estimated_arv,
        "avg_price_per_sqft": round(avg_price_per_sqft, 2),
        "comps_count_used": len(comps_df),
        "comps": comps_used
    }
