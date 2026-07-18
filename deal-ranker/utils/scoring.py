import pandas as pd

def calculate_mao(arv, repairs, mao_percentage):
    return (arv * mao_percentage) - repairs

def evaluate_deal_metrics(lead, config):
    asking_price = float(lead.get('price', 0))
    arv = float(lead.get('arv', asking_price))
    repairs = float(lead.get('repairs', 0))
    year_built = lead.get('year_built')
    
    # Safely convert 'in_buy_box' parameter to a boolean
    in_buy_box = str(lead.get('in_buy_box', True)).lower() == 'true'
    
    mao = calculate_mao(arv, repairs, config['mao_percentage'])
    financial_gap = asking_price - mao

    # 1. New Four-Tier Prioritization Model
    if not in_buy_box:
        tier = 4  # Bottom Tier: Out of Buy Box
    elif asking_price <= mao:
        tier = 1  # Top Tier: Home Run (Fits Buy Box & Under MAO)
    elif financial_gap <= (mao * 0.30):
        tier = 2  # Mid Tier: Negotiable (Fits Buy Box & Close to MAO)
    else:
        tier = 3  # Low Tier: Wide Gap (Fits Buy Box but way overpriced)

    # 2. Component A: Margin Efficiency (Max 60 Points)
    if tier == 1:
        price_score = 60.0
    elif tier == 4:
        # Out of buy box properties can still calculate a price score based on their discount margin
        excess_pct = (asking_price - mao) / mao if mao > 0 else 1.0
        price_score = max(0.0, min(60.0, 60.0 * (1.0 - (excess_pct / 0.30))))
    else:
        excess_pct = (asking_price - mao) / mao
        price_score = max(0.0, min(60.0, 60.0 * (1.0 - (excess_pct / 0.30))))

    # 3. Component B: Buy Box Target Alignment (Max 25 Points Total)
    buy_box_fit_score = 0.0
    
    # Soft Filter Rule: Automatically strip all physical points if the property is out of the buy box
    if in_buy_box:
        # Sub-Score 1: Structural Layout Match (10 Points)
        if int(lead.get('beds', 0)) >= config.get('buy_box_beds', 0) and float(lead.get('baths', 0)) >= config.get('buy_box_baths', 0):
            buy_box_fit_score += 10.0
            
        # Sub-Score 2: Size Volume Fit (10 Points)
        if int(lead.get('sqft', 0)) >= config.get('buy_box_min_sqft', 0):
            buy_box_fit_score += 10.0
            
        # Sub-Score 3: Acreage Allocation Fit (5 Points)
        if config.get('buy_box_min_lot_size') is not None:
            prop_lot = lead.get('lot_size')
            if prop_lot and not pd.isna(prop_lot) and float(prop_lot) >= config['buy_box_min_lot_size']:
                buy_box_fit_score += 5.0
        else:
            buy_box_fit_score += 5.0
    else:
        buy_box_fit_score = 0.0  # Flat 0 points for physical alignment if out of buy box

    # 4. Component C: Age Risk Index Calculation (Max 15 Points)
    if year_built and not pd.isna(year_built):
        year = int(year_built)
        if year >= config['modern_year_cutoff']:
            age_score = 15.0
        elif year <= config['legacy_year_cutoff']:
            age_score = 0.0
        else:
            span = config['modern_year_cutoff'] - config['legacy_year_cutoff']
            age_score = 15.0 * ((year - config['legacy_year_cutoff']) / span)
    else:
        age_score = 7.5

    total_score = round(price_score + buy_box_fit_score + age_score, 2)
    return tier, total_score, financial_gap, round(mao, 2)
