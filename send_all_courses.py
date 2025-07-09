#!/usr/bin/env python3
"""
Script to send all available courses to Telegram
"""

from udemypy.database import database, settings as db_settings
from udemypy import settings
from udemypy.sender import TelegramBot
from udemypy import send_courses

def send_all_courses_to_telegram():
    """Send all available courses to Telegram channel"""
    
    print("🚀 Starting to send all available courses to Telegram...")
    
    try:
        # Connect to database
        print("📊 Connecting to database...")
        db = database.connect()
        
        # Get all courses
        all_courses = database.retrieve_courses(db)
        print(f"📚 Total courses in database: {len(all_courses)}")
        
        # Get courses already shared to Telegram
        shared_courses = database.retrieve_courses_shared_to_social_media(db, db_settings.TELEGRAM_NAME)
        available_courses = [c for c in all_courses if c.id not in [sc.id for sc in shared_courses]]
        
        print(f"📤 Courses available to share to Telegram: {len(available_courses)}")
        
        if not available_courses:
            print("✅ No courses available to share - all courses have already been shared!")
            return
        
        # Create Telegram bot
        print("🤖 Creating Telegram bot...")
        bot = TelegramBot(
            settings.TOKEN,
            settings.CHANNEL_ID,
            settings.CHANNEL_LINK,
            settings.GITHUB_LINK,
            settings.WHATSAPP_LINK,
        )
        
        # Connect bot
        print("🔗 Connecting to Telegram...")
        bot.connect()
        
        # Send all available courses
        print(f"📤 Sending {len(available_courses)} courses to Telegram...")
        send_courses.send_courses(
            db,
            bot,
            db_settings.TELEGRAM_NAME,
            db_settings.TELEGRAM_ID,
        )
        
        print("✅ All courses sent successfully!")
        
        # Show summary
        final_shared = database.retrieve_courses_shared_to_social_media(db, db_settings.TELEGRAM_NAME)
        print(f"📊 Summary: {len(final_shared)} total courses now shared to Telegram")
        
        db.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\nTroubleshooting:")
        print("1. Check if your Telegram bot token is valid")
        print("2. Make sure your bot is added as admin to the channel")
        print("3. Verify the channel ID is correct")
        print("4. Check if the bot has permission to send messages")

if __name__ == "__main__":
    send_all_courses_to_telegram() 