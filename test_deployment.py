#!/usr/bin/env python3
"""
Test script to verify deployment will work
"""

import os
import sys

def test_imports():
    """Test if all required modules can be imported"""
    print("🔍 Testing imports...")
    
    try:
        import udemypy
        import udemypy.database
        import udemypy.udemy
        import udemypy.sender
        print("✅ All modules imported successfully!")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_settings():
    """Test if settings can be loaded"""
    print("\n🔍 Testing settings...")
    
    try:
        from udemypy import settings
        print("✅ Settings loaded successfully!")
        
        # Check if required settings are available
        required_settings = ['TOKEN', 'CHANNEL_ID', 'CHANNEL_LINK']
        missing = []
        
        for setting in required_settings:
            if not hasattr(settings, setting) or not getattr(settings, setting):
                missing.append(setting)
        
        if missing:
            print(f"⚠️  Missing settings: {', '.join(missing)}")
            return False
        else:
            print("✅ All required settings are available!")
            return True
            
    except Exception as e:
        print(f"❌ Settings error: {e}")
        return False

def test_database():
    """Test database connection"""
    print("\n🔍 Testing database...")
    
    try:
        from udemypy.database import database
        db = database.connect()
        print("✅ Database connection successful!")
        db.close()
        return True
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False

def test_scheduler():
    """Test if scheduler can be imported"""
    print("\n🔍 Testing scheduler...")
    
    try:
        from udemypy.scheduler import schedule_bots, TelegramHandler
        print("✅ Scheduler imported successfully!")
        return True
    except Exception as e:
        print(f"❌ Scheduler error: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Deployment Test Suite")
    print("=" * 40)
    
    tests = [
        test_imports,
        test_settings,
        test_database,
        test_scheduler
    ]
    
    all_passed = True
    for test in tests:
        if not test():
            all_passed = False
    
    print("\n" + "=" * 40)
    if all_passed:
        print("🎉 All tests passed! Your deployment should work!")
        print("\n📋 Next steps:")
        print("1. Commit and push your changes")
        print("2. Redeploy on Render")
        print("3. Your bot should start working!")
    else:
        print("❌ Some tests failed. Please fix the issues above.")
        sys.exit(1)

if __name__ == "__main__":
    main() 