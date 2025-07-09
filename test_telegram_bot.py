#!/usr/bin/env python3
"""
Test script to check Telegram bot configuration and send a test course
"""

from udemypy.database import database
from udemypy.database import settings as db_settings
from udemypy import settings
from udemypy.sender import TelegramBot
from udemypy import send_courses

def test_telegram_bot():
    """Test Telegram bot configuration and send a test course"""
    
    print("Testing Telegram Bot Configuration...")
    
    # Check if required environment variables are set
    print(f"TOKEN: {'✅ Set' if settings.TOKEN else '❌ Not set'}")
    print(f"CHANNEL_ID: {'✅ Set' if settings.CHANNEL_ID else '❌ Not set'}")
    print(f"CHANNEL_LINK: {'✅ Set' if settings.CHANNEL_LINK else '❌ Not set'}")
    
    if not all([settings.TOKEN, settings.CHANNEL_ID, settings.CHANNEL_LINK]):
        print("\n❌ Missing required Telegram configuration!")
        print("Please check your .env file and ensure TOKEN, CHANNEL_ID, and CHANNEL_LINK are set.")
        return
    
    try:
        # Connect to database
        print("\nConnecting to database...")
        db = database.connect()
        
        # Get available courses
        all_courses = database.retrieve_courses(db)
        print(f"Total courses in database: {len(all_courses)}")
        
        # Get courses not shared to Telegram
        shared_courses = database.retrieve_courses_shared_to_social_media(db, db_settings.TELEGRAM_NAME)
        available_courses = [c for c in all_courses if c.id not in [sc.id for sc in shared_courses]]
        
        print(f"Courses available to share to Telegram: {len(available_courses)}")
        
        if not available_courses:
            print("❌ No courses available to share!")
            return
        
        # Create Telegram bot
        print("\nCreating Telegram bot...")
        bot = TelegramBot(
            settings.TOKEN,
            settings.CHANNEL_ID,
            settings.CHANNEL_LINK,
            settings.GITHUB_LINK,
            settings.WHATSAPP_LINK,
        )
        
        # Connect bot
        print("Connecting to Telegram...")
        bot.connect()
        
        # Send first available course as test
        test_course = available_courses[0]
        print(f"\nSending test course: {test_course.title}")
        
        bot.send_course(test_course)
        
        # Mark as shared in database
        from datetime import datetime
        database.add_course_social_media(
            db,
            test_course.id,
            db_settings.TELEGRAM_ID,
            datetime.now(),
        )
        
        print("✅ Test course sent successfully!")
        print(f"Course: {test_course.title}")
        print(f"Link: {test_course.link_with_coupon}")
        
        db.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\nTroubleshooting:")
        print("1. Check if your Telegram bot token is valid")
        print("2. Make sure your bot is added as admin to the channel")
        print("3. Verify the channel ID is correct")
        print("4. Check if the bot has permission to send messages")

if __name__ == "__main__":
    test_telegram_bot() 