# Buy Box Soft-Filtering Engine (Skill #4)

An automated data-tagging agent that evaluates property leads against custom, investor-defined criteria. Unlike traditional hard-filters that delete non-conforming leads, this skill implements a **soft-filter**—keeping 100% of your data intact while flag-tagging assets for downstream pipeline optimization.

## 🔄 The Soft-Filtering Paradigm
By labeling instead of discarding data, this engine ensures you never accidentally miss a massive discount opportunity simply because an asset sits slightly outside your ideal physical box. 
* Every processed property is preserved.
* Properties are injected with an `in_buy_box` (`True`/`False`) boolean flag.
* Failed properties receive an explicit `buy_box_fail_reason` string tracking exactly which metric missed the mark.

## Custom Initialization Rules
1. Copy `buy_box.example.json` and rename it to `buy_box.json`.
2. Populate the fields with your acquisition boundaries.
3. **Important Note on Optional Fields:** If you do not care about a specific metric (e.g., you do not care about a minimum lot acreage), set its value to `null` or delete the row. The engine will recognize this and skip that validation entirely.

### Supported Parameters
* `target_zip_codes`: A list of strings defining your target geographic footprint.
* `max_price`: The absolute financial ceiling for initial consideration.
* `min_beds` / `min_baths`: Minimum structural layout specifications.
* `min_sqft`: Minimum interior living space volume.
* `min_lot_size`: *(Optional)* Minimum land acreage threshold.
* `min_year_built`: Minimum property age boundary to control utility risk exposure.

## Pipeline Integration
When executed, this tool hooks directly into your data flow:
* **Intake:** Automatically pulls historical data ledgers from `mls-web-scraper` or `mls-deal-finder`.
* **Output:** Compiles and exports the fully annotated dataset directly to `processed_deals.csv` for seamless consumption by the `deal-ranker` module.

## ⚠️ Disclaimer
This script handles mathematical boundaries and data coordination. It cannot evaluate subjective real estate attributes like neighborhood aesthetic, local traffic patterns, or structural damage. **This open-source component is distributed for free with absolutely no software training, debugging guarantees, or individual platform setup support.**
