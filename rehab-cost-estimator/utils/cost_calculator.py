def calculate_rehab_estimate(vision_assessment, sqft, benchmarks):
    """
    Translates visual distress flags and living square footage into a concrete
    itemized dollar estimate using local contractor cost benchmarks.
    """
    rehab_level = vision_assessment.get("rehab_level", "medium")
    property_sqft = float(sqft or 1500)
    
    # 1. Square-foot baseline estimate
    if rehab_level == "light":
        base_cost = property_sqft * benchmarks.get("cosmetic_refresh_per_sqft", 15.0)
    elif rehab_level == "heavy":
        base_cost = property_sqft * benchmarks.get("heavy_gut_per_sqft", 65.0)
    elif rehab_level == "full_gut":
        base_cost = property_sqft * benchmarks.get("heavy_gut_per_sqft", 75.0)
    else:  # Medium / Default
        base_cost = property_sqft * benchmarks.get("medium_rehab_per_sqft", 35.0)

    # 2. Add itemized visual distress add-ons if specific major items flagged
    itemized_addons = 0.0
    if vision_assessment.get("needs_roof"):
        itemized_addons += benchmarks.get("roof_replacement", 8500.0)
    if vision_assessment.get("needs_kitchen") and rehab_level == "light":
        itemized_addons += benchmarks.get("full_kitchen_remodel", 12000.0)

    total_estimate = round(base_cost + itemized_addons, 2)
    return total_estimate
