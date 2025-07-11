import os

# Force SQLite3 for Render deployment
LOCAL_DATABASE_PATH = os.path.join("data", "courses.db")
DATABASE = "sqlite3"  # ✅ Force SQLite3 for Render
DATABASE_URL = os.getenv("DATABASE_URL", "mysql://root:@127.0.0.1:3308/tg_enroll")
COURSE_LIFETIME = os.getenv("COURSE_LIFETIME")
COURSE_LIFETIME = None if COURSE_LIFETIME is None else int(COURSE_LIFETIME)


RECONNECTION_ATTEMPTS = 4
COMMAND_EXECUTION_SLEEP_TIME = 4
UPDATE_DATABASE_COMMANDS = ("DELETE", "INSERT INTO", "CREATE TABLE", "DROP")

# social_media table
TWITTER_ID = 0
TELEGRAM_ID = 1
WHATSAPP_ID = 2
TWITTER_NAME = "Twitter"
TELEGRAM_NAME = "Telegram"
WHATSAPP_NAME = "WhatsApp"
