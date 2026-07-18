import logging

def normalize_distress_payload(raw_records):
    """
    Translates raw public court API records into the standardized 
    schema utilized by the buy-box-filter and deal-ranker modules.
    """
    normalized_list = []
    
    for item in raw_records:
        try:
            # Map values to match framework requirements
            address = item.get("property_address", item.get("address", "Unknown Address"))
            zip_code = item.get("zip_code", item.get("property_zip", ""))
            
            # Off-market legal entries often lack an explicit retail asking price.
            # We intelligently use estimated value or fallback on the legal opening bid.
            est_value = item.get("estimated_value_usd")
            opening_bid = item.get("opening_bid_usd")
            resolved_price = int(est_value or opening_bid or 0)
            
            lead = {
                "address": address,
                "zip_code": str(zip_code).strip(),
                "price": resolved_price,
                "beds": int(item.get("bedrooms", item.get("beds", 0)) or 0),
                "baths": float(item.get("bathrooms", item.get("baths", 0)) or 0.0),
                "sqft": int(item.get("living_area_sqft", item.get("sqft", 0)) or 0),
                "lot_size": float(item.get("lot_size_acres", 0.0)) if item.get("lot_size_acres") else None,
                "year_built": int(item.get("year_built", 0)) if item.get("year_built") else None,
                "property_type": item.get("property_type", "Single Family"),
                
                # Context metadata required for downstream comping and tracking
                "arv": resolved_price if resolved_price > 0 else 0,
                "repairs": int(item.get("lien_amount_usd", 0) or 0), # Fallback lien metrics as initial cost
                "distress_type": item.get("event_type", "Public Record Filing"),
                "case_number": item.get("case_number", "N/A")
            }
            
            # Strip junk data lacking actionable locations
            if address != "Unknown Address":
                normalized_list.append(lead)
                
        except Exception as e:
            logging.warning(f"Error compiling public record dictionary row: {e}")
            continue
            
    return normalized_list
