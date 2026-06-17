Real Estate Daily Scraper
An automated tool designed to scrape, clean, and consolidate daily real estate listings from major platforms (Zillow, Redfin, Trulia, and Compass). This tool automatically deduplicates listings using a normalized address engine to provide a single, clean CSV file for your market analysis.

⚠️ Important Disclaimer
Use this tool at your own risk. Many real estate websites have Terms of Service (ToS) that prohibit automated scraping. This tool is intended for educational and personal use only. You are responsible for ensuring your usage complies with the policies of the platforms you are querying and for managing your own IP/request rates to avoid being blocked.

Prerequisites
Python 3.9+ installed on your system.

A basic understanding of the command line/terminal.

Recommended: A professional scraping API key (e.g., ScraperAPI, Bright Data) if you plan to scrape at scale, as residential IP addresses are frequently blocked by real estate platforms.

Installation
Clone this repository:

Bash
git clone https://github.com/yourusername/real-estate-scraper.git
cd real-estate-scraper
Install dependencies:

Bash
pip install -r requirements.txt
Set up configuration:
Copy the example config file and add your target zip codes and preferences:

Bash
cp config.example.py config.py
Open config.py in your text editor and update the ZIP_CODES list.

Usage
Running Manually
To execute a scrape immediately:

Bash
python main.py
Scheduling
This script is designed to run daily. You can use your system's scheduler:

Linux/macOS (Cron):
Add this to your crontab -e to run every night at 10:00 PM:

Bash
0 22 * * * /usr/bin/python3 /path/to/your/main.py
Windows (Task Scheduler):
Create a "Basic Task" to run python.exe with main.py as the argument daily at 10 PM.

How it Works
Normalization Engine: Uses custom Regex logic to identify and standardize addresses (e.g., "N" to "North", "St" to "Street") while protecting ordinals (e.g., "51st" remains "51st").

Deduplication: Merges data from multiple sources and uses (Normalized Address + Price) as a unique key to prevent duplicate records.

Rate Limiting: Includes randomized wait times between requests to mimic human browsing behavior.

Troubleshooting
"429 Too Many Requests": You are scraping too fast. Increase the DELAY variable in config.py.

"Selector Errors": Real estate websites frequently update their structure. If the data isn't pulling correctly, check if the website layout has changed and update the CSS selectors in the scraping modules.

Created for the community. Contributions and improvements are welcome via Pull Requests.
