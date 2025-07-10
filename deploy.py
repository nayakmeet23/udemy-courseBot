#!/usr/bin/env python3
"""
Deployment Helper Script for UdemyPy
This script helps validate your setup before deployment
"""

import os
import sys
from dotenv import load_dotenv

def check_environment():
    """Check if all required environment variables are set"""
    print("🔍 Checking environment variables...")
    
    required_vars = [
        'TOKEN',
        'CHANNEL_ID', 
        'CHANNEL_LINK'
    ]
    
    optional_vars = [
        'GITHUB_LINK',
        'WHATSAPP_LINK',
        'PAGES_TO_SCRAPE',
        'FAST_MODE',
        'MAX_COURSES_TO_PROCESS',
        'MAX_COURSES_TO_SEND',
        'DATABASE'
    ]
    
    missing_required = []
    missing_optional = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_required.append(var)
    
    for var in optional_vars:
        if not os.getenv(var):
            missing_optional.append(var)
    
    if missing_required:
        print("❌ Missing required environment variables:")
        for var in missing_required:
            print(f"   - {var}")
        return False
    
    if missing_optional:
        print("⚠️  Missing optional environment variables:")
        for var in missing_optional:
            print(f"   - {var}")
        print("   (These will use default values)")
    
    print("✅ All required environment variables are set!")
    return True

def test_imports():
    """Test if all required modules can be imported"""
    print("\n🔍 Testing imports...")
    
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

def test_database_connection():
    """Test database connection"""
    print("\n🔍 Testing database connection...")
    
    try:
        from udemypy.database import database
        db = database.connect()
        print("✅ Database connection successful!")
        db.close()
        return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

def main():
    """Main deployment check function"""
    print("🚀 UdemyPy Deployment Checker")
    print("=" * 40)
    
    # Load environment variables from .env file if it exists
    if os.path.exists('.env'):
        load_dotenv()
        print("📄 Loaded .env file")
    
    # Run all checks
    checks = [
        check_environment,
        test_imports,
        test_database_connection
    ]
    
    all_passed = True
    for check in checks:
        if not check():
            all_passed = False
    
    print("\n" + "=" * 40)
    if all_passed:
        print("🎉 All checks passed! Your project is ready for deployment.")
        print("\n📋 Next steps:")
        print("1. Push your code to GitHub")
        print("2. Go to Railway.app and create a new project")
        print("3. Connect your GitHub repository")
        print("4. Set the environment variables in Railway dashboard")
        print("5. Deploy!")
    else:
        print("❌ Some checks failed. Please fix the issues above before deploying.")
        sys.exit(1)

if __name__ == "__main__":
    main() 