# Buy Box Filtering Engine (Skill #4)

An automated data-sifting agent that isolates premium properties based on custom, investor-defined acquisitions criteria.

## Custom Initialization Rules
1. Copy `buy_box.example.json` and rename it to `buy_box.json`.
2. Populate fields with your exact requirements.
3. **Important Note on Optional Fields:** If you do not care about a specific metric (e.g., you do not care how old the roof or wiring is), either delete that row from your json entirely or set its value to `null`. It will be completely ignored by the matching engine.

## Cross-Skill Integration
When launched, this tool connects directly with sister components in your `rei-skills` ecosystem:
* **Option 1 (MLS Integration):** Direct pathing pulls historical tracking files from the output datasets inside your `scraper-v1` tool directory automatically.
* **Option 2 (Generic Lists):** Clean mappings parse standard custom real estate lists.
* **Option 3 (Manual Intake):** Enables instant evaluation of manual leads right over your terminal console.

##Need help implementing this bot in your organization?  3 Degrees Consutling has a done for you service.  Please book a time at www.Go3DC.com


## ⚠️ Disclaimer
This script filters mathematical structures and coordinates. It cannot accurately evaluate subjective attributes like curb appeal, structural damage, or neighborhood vibe. **This open-source engine is provided for free with absolutely no software training, maintenance expectations, or technical setup support.**
