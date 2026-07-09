# Pipeline Deal Ranker (Skill #5)

An advanced algorithmic sorting manager that calculates Maximum Allowable Offers (MAO) and dynamically ranks real estate opportunities by structural risk, exact buy box alignment, and acquisition price gap spreads.

## Dynamic Pipeline Execution Mechanics
This script is engineered to interpret and sequence datasets passed directly down from upstream components:
1. Copy `ranker_config.example.json` and create your operational parameters profile named `ranker_config.json`.
2. The core framework automatically checks for input sequences coming out of your sister `buy-box-filter` directory.
3. Properties are classified into structural prioritization buckets:
   * **Tier 1 (🚨 Home Run Deals):** Properties where the seller's asking price sits at or below your target calculated MAO threshold.
   * **Tier 2 (Qualified Value Targets):** Properties passing physical criteria sorted entirely by the smallest margin gap distance to your buy price.
   * **Tier 3 (Marginal Discrepancies):** Properties carrying extreme price variances or structural age hazards.

## The 100-Point Optimization Formula
To organize multi-deal listings, a point array calculates structural weights:
* **Acquisition Efficiency (Max 60 Points):** Evaluates percentage margin alignment relative to target offer boundaries.
* **Buy Box Target Match (Max 25 Points):** Awards premium allocations to core buy box parameters (Bed/Bath metrics, Square Footage, and Lot Acreage).
* **Asset Age Risk (Max 15 Points):** Decreases exposure risk by tracking property year built criteria against environmental cutoff values.

## ⚠️ Disclaimer
This processing tool executes numerical computations based on user-provided pricing structures. It does not evaluate regional zoning changes or local municipal encumbrances. **This open-source repository asset is distributed completely free of charge with no assumptions of customized technical deployment assistance or platform usage training.**
