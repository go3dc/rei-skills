def matches_buy_box(prop, bb):
    """
    Evaluates a single property against the buy box configuration.
    If a buy box field is missing or null, it is treated as irrelevant 
    and skipped automatically.
    """
    # 1. Zip Code Check
    if bb.get("target_zip_codes"):
        if str(prop.get("zip_code")) not in [str(z) for z in bb["target_zip_codes"]]:
            return False, f"Zip code {prop.get('zip_code')} not in target list."

    # 2. Maximum Price Check
    if bb.get("max_price") is not None:
        if prop.get("price") and prop.get("price") > bb["max_price"]:
            return False, f"Price (${prop.get('price'):,}) exceeds maximum threshold (${bb['max_price']:,})."

    # 3. Minimum Bedrooms Check
    if bb.get("min_beds") is not None:
        if prop.get("beds") and prop.get("beds") < bb["min_beds"]:
            return False, f"Bedrooms ({prop.get('beds')}) below minimum requirement ({bb['min_beds']})."

    # 4. Minimum Bathrooms Check
    if bb.get("min_baths") is not None:
        if prop.get("baths") and prop.get("baths") < bb["min_baths"]:
            return False, f"Bathrooms ({prop.get('baths')}) below minimum requirement ({bb['min_baths']})."

    # 5. Minimum Square Footage Check
    if bb.get("min_sqft") is not None:
        if prop.get("sqft") and prop.get("sqft") < bb["min_sqft"]:
            return False, f"Square footage ({prop.get('sqft')}) below minimum requirement ({bb['min_sqft']})."

    # 6. Year Built Check
    if bb.get("min_year_built") is not None:
        if prop.get("year_built") and prop.get("year_built") < bb["min_year_built"]:
            return False, f"Year built ({prop.get('year_built')}) is older than threshold ({bb['min_year_built']})."

    # 7. Property Type Check
    if bb.get("property_types"):
        if prop.get("property_type") not in bb["property_types"]:
            return False, f"Property type '{prop.get('property_type')}' not in accepted criteria."

    return True, "Matches Buy Box parameters."
