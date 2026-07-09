def matches_buy_box(prop, bb):
    """
    Evaluates a single property against the updated location and size metrics.
    Skips any unconfigured or null fields automatically.
    """
    # 1. Target Zip Code Validation
    if bb.get("target_zip_codes"):
        if str(prop.get("zip_code")) not in [str(z) for z in bb["target_zip_codes"]]:
            return False, f"Zip code {prop.get('zip_code')} is outside the target area."

    # 2. Maximum Price Check
    if bb.get("max_price") is not None:
        if prop.get("price") and prop.get("price") > bb["max_price"]:
            return False, f"Price (${prop.get('price'):,}) exceeds maximum threshold."

    # 3. Structural Bed/Bath Requirements
    if bb.get("min_beds") is not None:
        if prop.get("beds") and prop.get("beds") < bb["min_beds"]:
            return False, f"Beds ({prop.get('beds')}) below requirement."
            
    if bb.get("min_baths") is not None:
        if prop.get("baths") and prop.get("baths") < bb["min_baths"]:
            return False, f"Baths ({prop.get('baths')}) below requirement."

    # 4. Square Footage Check
    if bb.get("min_sqft") is not None:
        if prop.get("sqft") and prop.get("sqft") < bb["min_sqft"]:
            return False, f"Square footage ({prop.get('sqft'):,}) below minimum threshold."

    # 5. Lot Size Acreage Check (Optional Component)
    if bb.get("min_lot_size") is not None:
        prop_lot = prop.get("lot_size")
        if prop_lot is not None and prop_lot < bb["min_lot_size"]:
            return False, f"Lot size ({prop_lot} acres) below minimum required acreage."

    # 6. Year Built Constraint
    if bb.get("min_year_built") is not None:
        if prop.get("year_built") and prop.get("year_built") < bb["min_year_built"]:
            return False, f"Year built is too old."

    return True, "Passed all core buy box specifications."
