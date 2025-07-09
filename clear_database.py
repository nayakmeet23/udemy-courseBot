#!/usr/bin/env python3
"""
Script to clear database data while preserving table structure
"""

from udemypy.database import database

def clear_database_data():
    """Clear all data from database tables while preserving structure"""
    print("🗑️  Clearing database data...")
    
    # Connect to database
    db = database.connect()
    
    try:
        # Clear course_social_media first (due to foreign key constraints)
        print("  - Clearing course_social_media table...")
        db.execute("DELETE FROM course_social_media", commit=True)
        
        # Clear courses table
        print("  - Clearing course table...")
        db.execute("DELETE FROM course", commit=True)
        
        # Reset auto-increment counters
        print("  - Resetting auto-increment counters...")
        db.execute("ALTER TABLE course AUTO_INCREMENT = 1", commit=True)
        db.execute("ALTER TABLE course_social_media AUTO_INCREMENT = 1", commit=True)
        
        print("✅ Database data cleared successfully!")
        print("📊 Tables structure preserved.")
        
    except Exception as e:
        print(f"❌ Error clearing database: {e}")
        return False
    
    finally:
        db.close()
    
    return True

if __name__ == "__main__":
    # Ask for confirmation
    print("⚠️  WARNING: This will delete ALL course data from your database!")
    print("   Tables structure will be preserved.")
    confirm = input("   Are you sure you want to continue? (yes/no): ")
    
    if confirm.lower() in ['yes', 'y']:
        clear_database_data()
    else:
        print("❌ Operation cancelled.") 