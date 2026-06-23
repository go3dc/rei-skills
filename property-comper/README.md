# Property Comper (Skill #2)

An automated valuation engine that calculates the After Repair Value (ARV) of a target property using local, historical sold data. 

## How to Use
1. Copy `target_property.json` and fill in your subject property's specifications (including coordinates).
2. Go to Zillow or Redfin, filter by "Recently Sold" in your neighborhood, click "Download All" to get a CSV file, and save it in this directory as `historical_solds.csv`.
3. Run the script:
   ```bash
   python main.py


##   ⚠️ Disclaimer
This tool provides a baseline mathematical valuation. It does not account for property condition, material finishes, or hyper-local neighborhood factors (e.g., being next to a train track). Use this data as a starting point, not financial advice. No support or training is provided for this free tool.
