# Real Estate Daily Scraper

An automated, resilient agent for gathering market intelligence from real estate platforms. This tool scrapes, cleans, and consolidates daily listings from Zillow, Redfin, Trulia, and Compass, producing a clean, deduplicated CSV for your analysis.

## Extended Description
This project is built to solve the "data inconsistency" problem in real estate scraping.
* **Normalization Engine:** Raw addresses from different sites vary wildly. Our engine uses regex to standardize formats while protecting ordinals (e.g., "51st") to ensure high-accuracy deduplication.
* **Resilient Pipeline:** Traditional scrapers crash when encountering errors. This agent utilizes a `state_manager` to track progress, allowing the script to resume exactly where it left off if interrupted.
* **Observability:** With centralized logging and metrics, users can monitor the health and performance of their scrapes, ensuring they are always operating within site-specific rate limits.

## ⚠️ Important Disclaimer
**Use this tool at your own risk.** Many real estate websites have Terms of Service (ToS) that prohibit automated scraping. This tool is intended for **educational and personal use only**. You are responsible for ensuring your usage complies with the policies of the platforms you are querying and for managing your own IP/request rates to avoid being blocked.
**No Support or Warranty:** This tool is provided "as-is," completely free of charge. There is no expectation of support, training, or technical assistance. We CAN provide help with personal setups, dubugging, or custom modifications for a fee.  Please contact us at www.go3dc.com to discuss getting paid support with us for this tool.

## Prerequisites
* **Python 3.9+** installed on your system.
* A basic understanding of the command line/terminal.
* **Recommended:** A professional scraping API key (e.g., ScrapingBee, ScraperAPI, ZenRows) if you plan to scrape at scale.

## Installation
1. **Clone this repository:**
   ```bash
   git clone [https://github.com/yourusername/real-estate-scraper.git](https://github.com/yourusername/real-estate-scraper.git)
   cd real-estate-scraper

Install dependencies:

Bash
pip install -r requirements.txt


Set up configuration:
Copy the example config file and add your target zip codes and preferences:

Bash
cp config.example.py config.py
Open config.py in your text editor and update the ZIP_CODES list.

Proxy Support (Optional)
If you are scraping many zip codes, you may need a proxy service to avoid being blocked.

Get a Proxy Provider: We recommend services like ScrapingBee, ScraperAPI, or ZenRows (all offer generous free tiers).

Configure: In config.py, set USE_PROXY = True and paste your provider's PROXY_URL.

Note on Free Proxies: We advise against using "free public proxy lists" found online, as they are often unstable, slow, and potentially malicious.

Usage
Running Manually
To execute a scrape immediately:

Bash
python main.py
Scheduling
This script is designed to run daily.

Linux/macOS (Cron): Add this to your crontab -e to run every night at 10:00 PM:

Bash
0 22 * * * /usr/bin/python3 /path/to/your/main.py
Windows (Task Scheduler): Create a "Basic Task" to run python.exe with main.py as the argument daily at 10 PM.

How it Works
Normalization Engine: Uses Regex logic to standardize addresses while protecting ordinals.

State Persistence: Tracks processed zip codes in state.json to allow for seamless task resumption.

Observability: Logs performance metrics in logs/metrics.log to track your scrape history.

Anti-Bot Deception: Implements rotating headers and randomized delays to mimic human browsing.

Troubleshooting
"429 Too Many Requests": You are scraping too fast. Increase the delay or enable the USE_PROXY option in config.py.

"Selector Errors": If the website layout changes, the data will not pull correctly. Check the logs/scraper.log for details.

Created for the community. Contributions and improvements are welcome via Pull Requests.

This skill is provided for free with no expectation implied or otherwise of support.  It is provided for informational purpopses only.  Please note that every 
