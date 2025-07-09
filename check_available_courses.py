#!/usr/bin/env python3
"""
Script to check what courses are available to be shared
"""

from udemypy.database import database
from udemypy.database import settings as db_settings

def check_available_courses():
    """Check what courses are available to be shared"""
    
    try:
        # Connect to database
        print("Connecting to database...")
        db = database.connect()
        
        # Get all courses
        all_courses = database.retrieve_courses(db)
        print(f"Total courses in database: {len(all_courses)}")
        
        # Check courses for each social media platform
        social_platforms = [
            ("Telegram", db_settings.TELEGRAM_NAME),
            ("Twitter", db_settings.TWITTER_NAME),
            ("WhatsApp", db_settings.WHATSAPP_NAME)
        ]
        
        for platform_name, platform_id in social_platforms:
            try:
                shared_courses = database.retrieve_courses_shared_to_social_media(db, platform_id)
                available_courses = [c for c in all_courses if c.id not in [sc.id for sc in shared_courses]]
                
                print(f"\n{platform_name}:")
                print(f"  - Shared courses: {len(shared_courses)}")
                print(f"  - Available to share: {len(available_courses)}")
                
                if available_courses:
                    print(f"  - Sample available courses:")
                    for i, course in enumerate(available_courses[:3]):  # Show first 3
                        print(f"    {i+1}. {course.title}")
                    if len(available_courses) > 3:
                        print(f"    ... and {len(available_courses) - 3} more")
                        
            except Exception as e:
                print(f"  - Error checking {platform_name}: {e}")
        
        # Show some sample courses from database
        print(f"\nSample courses in database:")
        for i, course in enumerate(all_courses[:5]):  # Show first 5
            print(f"  {i+1}. {course.title}")
            print(f"     Link: {course.link}")
            print(f"     Coupon: {course.coupon_code}")
            print(f"     Date: {course.date_found}")
            print()
        
        db.close()
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_available_courses() 