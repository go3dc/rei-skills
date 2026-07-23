import os
import re
import pandas as pd
from utils.comp_finder import CompAnalysisResult

def sanitize_filename(name: str) -> str:
    clean = re.sub(r'[^a-zA-Z0-9]', '_', name)
    return re.sub(r'_+', '_', clean).strip('_').lower()

def generate_individual_reports(subject_property: dict, comp_result: CompAnalysisResult, config):
    """
    Generates standalone Markdown and CSV comp reports for a single property project.
    """
    os.makedirs(config.REPORTS_DIR, exist_ok=True)
    raw_address = subject_property.get("address", "property")
    file_stub = sanitize_filename(raw_address)

    # 1. Generate Markdown Report
    if config.GENERATE_MARKDOWN_REPORTS:
        md_filename = os.path.join(config.REPORTS_DIR, f"comps_{file_stub}.md")
        
        md_content = f"""# Comparable Market Analysis (CMA) Report

## Subject Property Overview
* **Address:** {subject_property.get('address', 'N/A')}, {subject_property.get('zip_code', '')}
* **Specs:** {subject_property.get('beds', 'N/A')} Beds | {subject_property.get('baths', 'N/A')} Baths | {subject_property.get('sqft', 'N/A'):,} SqFt
* **Property Type:** {subject_property.get('property_type', 'Single Family')}
* **Year Built:** {subject_property.get('year_built', 'N/A')}
* **Current Asking Price:** ${int(subject_property.get('price', 0)):,}

---

## Valuation & ARV Determination
* **Calculated ARV:** **${int(comp_result.estimated_arv):,}**
* **Average Price / SqFt:** ${comp_result.arv_price_per_sqft:.2f} / sqft
* **Valuation Summary:** {comp_result.valuation_summary}

---

## Comparable Sales Used in Valuation

"""
        for idx, comp in enumerate(comp_result.comps, 1):
            md_content += f"""### Comp #{idx}: {comp.address}
* **Sale Price:** ${int(comp.sale_price):,}
* **Sale Date / Frame:** {comp.sale_date}
* **Distance:** {comp.distance_miles:.2f} miles from subject
* **Specs:** {comp.beds} Beds | {comp.baths} Baths | {comp.sqft:,} SqFt
* **Price / SqFt:** ${comp.price_per_sqft:.2f}
* **Selection Rationale:** {comp.selection_rationale}

---
"""
        with open(md_filename, "w", encoding="utf-8") as f:
            f.write(md_content)

    # 2. Generate CSV Report
    if config.GENERATE_CSV_REPORTS:
        csv_filename = os.path.join(config.REPORTS_DIR, f"comps_{file_stub}.csv")
        
        comp_rows = []
        for comp in comp_result.comps:
            comp_rows.append({
                "subject_address": raw_address,
                "comp_address": comp.address,
                "sale_price": comp.sale_price,
                "sale_date": comp.sale_date,
                "beds": comp.beds,
                "baths": comp.baths,
                "sqft": comp.sqft,
                "price_per_sqft": comp.price_per_sqft,
                "distance_miles": comp.distance_miles,
                "selection_rationale": comp.selection_rationale
            })
            
        pd.DataFrame(comp_rows).to_csv(csv_filename, index=False)
