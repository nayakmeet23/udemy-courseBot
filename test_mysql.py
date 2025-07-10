#!/usr/bin/env python3
"""
Test MySQL connection and installation
"""

import os
import sys

def test_mysql_installation():
    """Test if MySQL connector is installed"""
    print("🔍 Testing MySQL connector installation...")
    
    try:
        import mysql.connector
        print("✅ MySQL connector installed successfully")
        print(f"   Version: {mysql.connector.__version__}")
        return True
    except ImportError as e:
        print(f"❌ MySQL connector not installed: {e}")
        return False

def test_mysql_connection():
    """Test MySQL connection"""
    print("\n🔍 Testing MySQL connection...")
    
    try:
        from udemypy.database import database
        from udemypy.database import settings
        
        print(f"   Database: {settings.DATABASE}")
        print(f"   Database URL: {settings.DATABASE_URL}")
        
        db = database.connect()
        print("✅ MySQL connection successful!")
        db.close()
        return True
        
    except Exception as e:
        print(f"❌ MySQL connection failed: {e}")
        return False

def main():
    """Run MySQL tests"""
    print("🗄️  MySQL Connection Test")
    print("=" * 40)
    
    # Test installation
    if not test_mysql_installation():
        print("\n❌ MySQL connector not installed!")
        print("   Please install: pip install mysql-connector-python==8.2.0")
        sys.exit(1)
    
    # Test connection
    if not test_mysql_connection():
        print("\n❌ MySQL connection failed!")
        print("   Please check your DATABASE_URL environment variable")
        sys.exit(1)
    
    print("\n🎉 All MySQL tests passed!")
    print("✅ Your deployment should work with MySQL!")

if __name__ == "__main__":
    main() 