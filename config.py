import os
import sys
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def has_openai_key() -> bool:
    """Returns True if the OpenAI API Key is set."""
    return bool(OPENAI_API_KEY and OPENAI_API_KEY.strip() and "your_openai_api_key_here" not in OPENAI_API_KEY)

# Model configurations
DEFAULT_MODEL = "gpt-4o-mini"
SUPPORTED_MODELS = [
    "gpt-4o-mini",
    "gpt-4o"
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

def print_setup_warning():
    """Prints a styled warning if crucial API keys are missing."""
    if not has_openai_key():
        print("=" * 60)
        print("⚠️  WARNING: OPENAI_API_KEY is not set in your .env file!")
        print("Please follow these steps to set up:")
        print("  1. Create an API key at: https://platform.openai.com/")
        print("  2. Open the '.env' file in this directory.")
        print("  3. Add your key: OPENAI_API_KEY=sk-proj-...")
        print("=" * 60)
