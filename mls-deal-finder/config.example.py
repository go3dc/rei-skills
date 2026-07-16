# Apify Authentication Settings
APIFY_TOKEN = "your_apify_api_token_here"

# The specific Apify actor target (e.g., apify/zillow-scraper or a dedicated MLS actor)
ACTOR_ID = "apify/zillow-scraper"

# Search Parameters
TARGET_LOCATIONS = ["90210", "10001"]
MAX_ITEMS_PER_LOCATION = 50

# Optional API filters allowed by the actor context
TYPE_FILTER = "ALL"  # Options typically include: "SALE", "RENT", "SOLD"
