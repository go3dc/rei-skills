# Public Records Distress Monitor

An API-driven off-market ingestion module that links directly to county court and municipal open-data registries to capture raw public filings, court actions, and distress event signals.

## Operational Overview
This skill acts as a high-intent, off-market lead alternative to traditional MLS scraping. It queries unified government open-data networks to aggregate raw legal updates directly from county record systems before those properties are listed publicly.

## System Integration Setup
1. Create an account on Apify and subscribe to a **paid platform tier** to handle database querying allocations.
2. Copy `config.example.py` to `config.py` and input your security token credentials.
3. Define your target geography using the county and state array properties:
   ```python
   TARGET_STATES = ["MD", "IL"]
   TARGET_COUNTIES = ["Prince George's", "Cook"]

