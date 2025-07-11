from os import getenv
import os
from pathlib import Path

# Get the project root directory (where .env file should be)
PROJECT_ROOT = Path(__file__).parent.parent
ENV_FILE = PROJECT_ROOT / '.env'

# Load environment variables from .env file
if ENV_FILE.exists():
    try:
        from dotenv import load_dotenv
        load_dotenv(ENV_FILE)
        print(f"[Settings] ✅ Loaded environment variables from {ENV_FILE}")
    except ImportError:
        print("[Settings] ⚠️  python-dotenv not installed, skipping .env file")
        print("[Settings] 💡 Run: pip install python-dotenv")
    except Exception as e:
        print(f"[Settings] ❌ Error loading .env file: {e}")
else:
    print(f"[Settings] ⚠️  .env file not found at {ENV_FILE}")
    print("[Settings] 💡 Create .env file with your bot credentials")

# === Sender Bots ===
GITHUB_LINK = "https://github.com/dylannalex/udemypy"
WHATSAPP_LINK = "https://whatsapp.com/channel/0029VaHwvWZ7NoZsk8UOUl0z"

# === Telegram Bot Config ===
TOKEN = getenv("TOKEN")
CHANNEL_ID = getenv("CHANNEL_ID")
CHANNEL_LINK = getenv("CHANNEL_LINK")
DONATE_ME_LINK = getenv("DONATE_ME_LINK")

# === Optional Twitter Config ===
TWITTER_LINK = getenv("TWITTER_LINK")
API_KEY = getenv("API_KEY")
API_KEY_SECRET = getenv("API_KEY_SECRET")
ACCESS_TOKEN = getenv("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = getenv("ACCESS_TOKEN_SECRET")

# === Scraper Settings ===
PAGES_TO_SCRAPE = int(getenv("PAGES_TO_SCRAPE", 3))  # Default = 3 if not set
FREE_COURSE_DISCOUNT = 100

# === ChromeDriver & Browser Settings ===
CHROMEDRIVER_PATH = getenv("CHROMEDRIVER_PATH", "chromedriver.exe")
GOOGLE_CHROME_BIN = getenv("GOOGLE_CHROME_BIN", "")  # Optional
PAGE_LOAD_TIME = int(getenv("PAGE_LOAD_TIME", 5))  # Wait time in seconds

# Debug: Print loaded values (remove in production)
print(f"[Settings] 🔍 Environment check:")
print(f"   TOKEN: {TOKEN[:20] if TOKEN else '❌ Not found'}...")
print(f"   CHANNEL_ID: {CHANNEL_ID or '❌ Not found'}")
print(f"   CHANNEL_LINK: {CHANNEL_LINK or '❌ Not found'}")
print(f"   PAGES_TO_SCRAPE: {PAGES_TO_SCRAPE}")
