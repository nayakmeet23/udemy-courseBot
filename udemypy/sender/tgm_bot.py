import time
import asyncio
from telegram import Bot, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.error import TelegramError, RetryAfter, NetworkError
from telegram.request import HTTPXRequest

from udemypy.course import Course
from udemypy.sender.text import emojis
from udemypy.sender.bot import SenderBot
from udemypy.sender.text.markdown_validation import get_valid_text


def _message_title(
    title, link, rating, students, language, discount_time_left, badge
) -> str:
    message = [
        f"[{emojis.BOOKS}]({link}) {title}",
        f"{emojis.STAR} {rating}/5",
        f"{emojis.PEOPLE_SILHOUETTE} {students} students",
        f"{emojis.GLOBE} {language}",
        f"{emojis.HOURGLASS} Free for {discount_time_left}",
        f"Subscribe for more free Udemy courses {emojis.HEART}",
    ]

    # Add course badge (if any)
    _badge_index = 1
    if badge:
        message.insert(_badge_index, f"{emojis.TROPHY} {badge}")

    return "\n\n".join(message)


class TelegramBot(SenderBot):
    def __init__(
        self,
        token: str,
        channel_id: str,
        channel_link: str,
        github_link: str,
        whatsapp_link: str,
        sleep_time_per_course: int = 10,  # Increased default sleep time
    ):
        self.token = token
        self.channel_id = channel_id
        self.channel_link = channel_link
        self.github_link = github_link
        self.whatsapp_link = whatsapp_link
        self.sleep_time_per_course = sleep_time_per_course
        self.bot = None
        
        # Button texts
        self.get_course_button_text = f"Get course {emojis.PERSON_RUNNING}"
        self.share_button_text = f"Share channel {emojis.SPEAKING_HEAD}"
        self.github_repo_text = f"GitHub Repo {emojis.HAPPY_CAT}"
        self.whatsapp_repo_text = f"Free Courses on WhatsApp {emojis.SPARKLES}"

    def connect(self) -> None:
        try:
            # Configure HTTPX request with proper connection pool settings
            request = HTTPXRequest(
                connection_pool_size=8,  # Reduced pool size
                connect_timeout=30.0,
                read_timeout=30.0,
                write_timeout=30.0,
                pool_timeout=30.0,  # Increased pool timeout
            )
            
            # Create bot instance with custom request
            self.bot = Bot(token=self.token, request=request)
            print("[Telegram] Bot initialized successfully with optimized connection pool")
        except Exception as e:
            print(f"[Telegram] Connection failed: {e}")
            raise

    async def _send_message_with_retry(self, message_text: str, keyboard: InlineKeyboardMarkup, max_retries: int = 3):
        """Send message with retry logic and proper error handling"""
        for attempt in range(max_retries):
            try:
                await self.bot.send_message(
                    chat_id=self.channel_id,
                    text=message_text,
                    parse_mode="MarkdownV2",
                    reply_markup=keyboard,
                )
                print(f"[Telegram] ✅ Message sent successfully (attempt {attempt + 1})")
                return True
                
            except RetryAfter as e:
                wait_time = e.retry_after + 2  # Add extra buffer
                print(f"[Telegram] ⏳ Rate limited, waiting {wait_time} seconds...")
                await asyncio.sleep(wait_time)
                
            except NetworkError as e:
                wait_time = (attempt + 1) * 5  # Exponential backoff
                print(f"[Telegram] 🌐 Network error (attempt {attempt + 1}/{max_retries}), waiting {wait_time}s: {e}")
                await asyncio.sleep(wait_time)
                
            except TelegramError as e:
                print(f"[Telegram] ❌ Telegram error (attempt {attempt + 1}/{max_retries}): {e}")
                if attempt == max_retries - 1:
                    raise
                await asyncio.sleep(5)
                
            except Exception as e:
                print(f"[Telegram] ❌ Unexpected error (attempt {attempt + 1}/{max_retries}): {e}")
                if attempt == max_retries - 1:
                    raise
                await asyncio.sleep(5)
        
        return False

    def send_course(self, course: Course) -> None:
        try:
            # Prepare course data
            course_title = get_valid_text(course.title)
            course_link = get_valid_text(course.link_with_coupon)
            course_language = get_valid_text(course.language)
            course_rating = get_valid_text(course.rating)
            course_students = get_valid_text(course.students)
            course_discount_time_left = get_valid_text(course.discount_time_left)
            course_badge = course.badge

            # Create buttons
            get_course_button = InlineKeyboardButton(
                text=self.get_course_button_text, url=course.link_with_coupon
            )
            share_button = InlineKeyboardButton(
                text=self.share_button_text, url=self.channel_link
            )
            github_button = InlineKeyboardButton(
                text=self.github_repo_text, url=self.github_link
            )
            whatsapp_button = InlineKeyboardButton(
                text=self.whatsapp_repo_text, url=self.whatsapp_link
            )

            # Create message content
            message_text = _message_title(
                course_title,
                course_link,
                course_rating,
                course_students,
                course_language,
                course_discount_time_left,
                course_badge,
            )
            
            # Create keyboard markup
            keyboard = InlineKeyboardMarkup([
                [get_course_button],
                [share_button, github_button],
                [whatsapp_button]
            ])
            
            # Send message with proper async handling
            async def send_async():
                await self._send_message_with_retry(message_text, keyboard)
            
            # Run async function
            try:
                # Try to use existing event loop
                loop = asyncio.get_event_loop()
                if loop.is_running():
                    # If loop is running, create a new task
                    asyncio.create_task(send_async())
                else:
                    # If loop is not running, run it
                    loop.run_until_complete(send_async())
            except RuntimeError:
                # No event loop, create new one
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                try:
                    loop.run_until_complete(send_async())
                finally:
                    loop.close()
            
            # Wait between messages to avoid rate limiting
            print(f"[Telegram] ⏳ Waiting {self.sleep_time_per_course} seconds before next message...")
            time.sleep(self.sleep_time_per_course)
            
        except Exception as e:
            print(f"[Telegram] ❌ Failed to send course '{course.title}': {e}")
            raise
