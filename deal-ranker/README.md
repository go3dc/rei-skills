# Pipeline Deal Ranker

An advanced algorithmic underwriting manager that computes Maximum Allowable Offers (MAO) and sequences real estate opportunities using a sophisticated 100-point scoring algorithm and a 4-tier pipeline strategy.

## 🧮 The Financial Core (MAO Formula)
The engine automatically establishes an objective purchase boundary for every asset utilizing the standard Maximum Allowable Offer framework:

$$MAO = (\text{ARV} \times \text{mao\_percentage}) - \text{repairs}$$

* **ARV (After Repair Value):** Pulled dynamically from upstream tools or matched directly to the listing price if data is absent.
* **MAO Percentage:** Completely adjustable inside your configuration file (defaults to **70%**).
* **Repairs:** Subtracted directly from the equity allocation base to insulate investor margins.

---

## 📊 The Four-Tier Prioritization Hierarchy
After calculating the financial target boundaries, the ranker processes the soft-filtered data from `processed_deals.csv` and segments listings into four distinct actionable operational buckets:

| Priority Tier | Pipeline Classification | Core Entry Condition | Automated Sorting Rule |
| :--- | :--- | :--- | :--- |
| **Tier 1** | 🚨 **Home Run Deal** | In Buy Box AND Asking Price $\le$ MAO | Pushed directly to the top; sorted by highest score. |
| **Tier 2** | 📈 **Negotiable Target** | In Buy Box AND Asking Price is within 30% over MAO | Sorted by the smallest raw financial price gap. |
| **Tier 3** | 🔍 **Wide Price Gap** | In Buy Box AND Asking Price is > 30% over MAO | Sorted by the smallest raw financial price gap. |
| **Tier 4** | ⚠️ **Out of Buy Box** | Property failed one or more Buy Box checks | Permanently demoted to the bottom of the ledger. |

---

## 💯 The 100-Point Optimization Formula
To break ties and organize listings within individual tiers, properties receive a structural fitness score out of 100 points:

### 1. Acquisition Efficiency (Max 60 Points)
Measures how close the seller's asking price is to your calculated MAO. Tier 1 deals automatically receive the full 60 points. Tiers 2, 3, and 4 scale down linearly based on the size of the pricing overage.

### 2. Buy Box Target Match (Max 25 Points)
Evaluates physical architectural alignment with your ideal portfolio specifications. 
* **Note:** If a property has been flagged as `in_buy_box = False` by the soft-filter, its Buy Box alignment score is **instantly wiped to 0.0 points**, forcing it safely down the queue.
* Conformity weights are distributed across structural layout (10 points), living square footage (10 points), and lot acreage minimums (5 points).

### 3. Asset Age Risk Index (Max 15 Points)
Protects rehab capital from hidden legacy utility issues (like knob-and-tube wiring or cast-iron plumbing). It awards full points to modern properties built after your cutoff year, scaling down to 0 points for turn-of-the-century assets.

## Execution Requirements
1. Ensure your `buy-box-filter` has generated an updated `processed_deals.csv` ledger.
2. Initialize your local `ranker_config.json` profile to adjust variables.
3. Run `main.py` to compile your target lead tracking strategy.

## ⚠️ Disclaimer
This processing engine runs automated priority calculations based entirely on user-provided inputs and config benchmarks. **This open-source project component is provided "as-is" without any assumptions of tailored technical deployment assistance, codebase maintenance, or software usage training.**
