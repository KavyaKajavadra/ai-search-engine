import os
import sys
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API Keys
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GOOGLE_CSE_ID = os.getenv("GOOGLE_CSE_ID")

# Model configurations
# Defaulting to gemini-2.0-flash as it is the standard active model in 2026
DEFAULT_MODEL = "gemini-2.0-flash"
SUPPORTED_MODELS = [
    "gemini-2.0-flash",
    "gemini-1.5-flash",
    "gemini-1.5-pro"
]

# Search configurations
DEFAULT_SEARCH_LIMIT = 5
MAX_SEARCH_LIMIT = 10

# Scraping settings
SCRAPE_TIMEOUT = 10.0  # seconds
# Max characters to extract per website to control context token size
MAX_CHARS_PER_PAGE = 15000 
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

# History file
HISTORY_FILE = ".search_history.json"

def has_gemini_key() -> bool:
    """Returns True if the Gemini API Key is set."""
    return bool(GEMINI_API_KEY and GEMINI_API_KEY.strip() and "your_gemini_api_key_here" not in GEMINI_API_KEY)

def has_google_search_keys() -> bool:
    """Returns True if Google Custom Search keys are configured."""
    has_key = bool(GOOGLE_API_KEY and GOOGLE_API_KEY.strip() and "your_google" not in GOOGLE_API_KEY)
    has_cse = bool(GOOGLE_CSE_ID and GOOGLE_CSE_ID.strip() and "your_custom" not in GOOGLE_CSE_ID)
    return has_key and has_cse

def print_setup_warning():
    """Prints a styled warning if crucial API keys are missing."""
    if not has_gemini_key():
        print("=" * 60)
        print("⚠️  WARNING: GEMINI_API_KEY is not set in your .env file!")
        print("Please follow these steps to set up:")
        print("  1. Create a free API key at: https://aistudio.google.com/")
        print("  2. Open the '.env' file in this directory.")
        print("  3. Add your key: GEMINI_API_KEY=AIzaSy...")
        print("=" * 60)
