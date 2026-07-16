import logging

def normalize_api_data(raw_items):
    """
    Maps raw, heterogeneous property JSON keys from the Apify API response
    into the standard schema used across the rei-skills framework.
    """
    standardized_leads = []
    
    for item in raw_items:
        try:
            # Safely navigate nested API payload paths
            address = item.get("address", {}).get("streetAddress", item.get("address", "Unknown"))
            zip_code = item.get("address", {}).get("zipcode", item.get("zipcode", ""))
            
            lead = {
                "address": address,
                "zip_code": zip_code,
                "price": int(item.get("price", 0) or 0),
                "beds": int(item.get("bedrooms", item.get("beds", 0)) or 0),
                "baths": float(item.get("bathrooms", item.get("baths", 0)) or 0),
                "sqft": int(item.get("livingArea", item.get("sqft", 0)) or 0),
                "lot_size": float(item.get("lotSize", 0.0) or 0.0) if item.get("lotSize") else None,
                "year_built": int(item.get("yearBuilt", 0) or 0) if item.get("yearBuilt") else None,
                "property_type": item.get("homeType", "Single Family"),
                "arv": int(item.get("price", 0) or 0),  # Default baseline assumption
                "repairs": 0  # Initialized value placeholder for optimization pipelines
            }
            standardized_leads.append(lead)
        except Exception as e:
            logging.warning(f"Skipping record due to formatting error: {e}")
            continue
            
    return standardized_leads
