import os

# Provider Configuration: "auto", "anthropic", "openrouter", or "openai"
# Set to "auto" to automatically infer from environment variables
PROVIDER = "auto"

# Default Model Selection (e.g., "claude-3-5-haiku-20241022", "anthropic/claude-haiku-4.5", "gpt-4o")
MODEL_NAME = "claude-3-5-haiku-20241022"

# API Keys (Fallback if not already present in Agent environment)
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", None)  # e.g., "http://localhost:8642/v1" for Hermes local gateway

# Search Parameters
MAX_COMPS_PER_PROPERTY = 4
MAX_SEARCH_RADIUS_MILES = 1.0
MAX_SALE_AGE_MONTHS = 6

# Output Preferences
REPORTS_DIR = "reports"
GENERATE_MARKDOWN_REPORTS = True
GENERATE_CSV_REPORTS = True
