from os import getenv
import os

# Try to load environment variables from .env file (only in development)
if os.path.exists('.env'):
    try:
        from dotenv import load_dotenv
        load_dotenv()  # ✅ Fixed: This line was outside the try block
    except ImportError:
        # If dotenv is not available, continue without it
        pass

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
