# MLS Deal Finder API Suite (Skill #6)

An official API-driven property ingestion engine that queries the Apify platform to retrieve up-to-date real estate listings directly without relying on fragile browser-level web scraping patterns.

## Architecture and Integration Setup
This asset functions as an institutional-grade data ingestion replacement for the base `scraper-v1` manual crawler. It normalizes real-time market data instantly into the format required by your automated analysis scripts:
1. Register for an account on [Apify](https://apify.com) and copy your security token key from your account dashboard console.
2. Copy `config.example.py` to `config.py` and paste your token credential inside the variable parameters.
3. Configure your targeted zip codes array list, select your preferred real estate data Actor ID, and launch the primary execution thread:
   ```bash
   python main.py
