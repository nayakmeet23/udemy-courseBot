from time import sleep
from abc import abstractmethod
from abc import ABC
from datetime import datetime, timedelta

from udemypy import send_courses
from udemypy import find_courses
from udemypy.database import database
from udemypy.database import settings as db_settings
from udemypy.udemy import settings as ud_settings
from udemypy import settings
from udemypy.sender import TelegramBot, WhatsAppBot
from udemypy.utils import clear_console
from udemypy.database import setup  # ✅ Add this import


class BotHandler(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def send_courses(self, db):
        pass


class TelegramHandler(BotHandler):
    def __init__(self):
        # Add type checking for environment variables
        if not settings.TOKEN:
            raise ValueError("TOKEN environment variable is required")
        if not settings.CHANNEL_ID:
            raise ValueError("CHANNEL_ID environment variable is required")
        if not settings.CHANNEL_LINK:
            raise ValueError("CHANNEL_LINK environment variable is required")
            
        self.bot = TelegramBot(
            token=settings.TOKEN,
            channel_id=settings.CHANNEL_ID,
            channel_link=settings.CHANNEL_LINK,
            github_link=settings.GITHUB_LINK,
            whatsapp_link=settings.WHATSAPP_LINK,
        )

    def send_courses(self, db):
        print("[Telegram Bot]")
        self.bot.connect()  # Reconnects every iteration
        send_courses.send_courses(
            db,
            self.bot,
            db_settings.TELEGRAM_NAME,
            db_settings.TELEGRAM_ID,
        )


class WhatsAppHandler(BotHandler):
    def __init__(self):
        # Add type checking for chromedriver path
        chromedriver_path = ud_settings.CHROMEDRIVER_PATH or "chromedriver.exe"
        self.whatsapp_bot = WhatsAppBot(chromedriver_path)
        self.whatsapp_bot.connect()  # Only first connection

    def send_courses(self, db):
        # WhatsApp Bot
        print("[WhatsApp Bot]")
        send_courses.send_courses(
            db,
            self.whatsapp_bot,
            db_settings.WHATSAPP_NAME,
            db_settings.WHATSAPP_ID,
        )


def setup_database_if_needed():
    """Setup database tables if they don't exist"""
    try:
        db = database.connect()
        # Try to query the course table to see if it exists
        db.execute("SELECT COUNT(*) FROM course", commit=False)
        print("[Database] Tables already exist")
    except Exception as e:
        if "no such table" in str(e).lower():
            print("[Database] Tables don't exist, creating them...")
            setup.setup_database()
            print("[Database] Tables created successfully")
        else:
            print(f"[Database] Error checking tables: {e}")
            raise


def schedule_bots(
    bot_handlers: list[BotHandler],
    waiting_seconds: int = 60 * 30,  # 30 min default
    iterations: int = 10,
):
    # ✅ Setup database tables if they don't exist
    setup_database_if_needed()
    
    db = database.connect()

    for iteration in range(iterations):
        # Find courses
        clear_console()
        print(f"[Iteration N°{iteration}]")
        print("[Finding Courses]")
        find_courses.find_courses(db, verbose=True)

        # Send courses
        for bot_handler in bot_handlers:
            bot_handler.send_courses(db)

        # Calculate the time of the next iteration
        next_iteration_time = datetime.now() + timedelta(seconds=waiting_seconds)
        next_iteration_time = next_iteration_time.strftime("%H:%M:%S")
        print(f"\n[-] Next iteration at: {next_iteration_time}")

        # Sleep
        sleep(waiting_seconds)

    db.close()


def run_scheduler():
    from udemypy.sender.tgm_bot import TelegramBot
    from udemypy.database import database, settings as db_settings
    from udemypy import settings as global_settings

    db = database.connect()
    telegram_bot = TelegramBot(
        token=global_settings.TOKEN,
        channel_id=global_settings.CHANNEL_ID,
        channel_link=global_settings.CHANNEL_LINK,
        github_link=global_settings.GITHUB_LINK,
        whatsapp_link=global_settings.WHATSAPP_LINK,
        sleep_time_per_course=10,
    )
    telegram_bot.connect()

    # Call your scheduling logic here
    # For example, if you have a function like schedule_bots:
    schedule_bots(
        bot_handlers=[telegram_bot],
        waiting_seconds=60 * 30,  # 30 minutes
        iterations=1,  # Or whatever you want for a single run
    )

if __name__ == "__main__":
    run_scheduler()
