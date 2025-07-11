#!/usr/bin/env python3
"""
Simple Render deployment script
Uses SQLite3 for Render free tier
"""

import os
import sys

def main():
    """Main deployment function"""
    print("🚀 Starting UdemyPy Bot on Render...")
    
    # Check required environment variables
    required_vars = ['TOKEN', 'CHANNEL_ID', 'CHANNEL_LINK']
    missing = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing.append(var)
    
    if missing:
        print(f"❌ Missing required environment variables: {', '.join(missing)}")
        print("Please set these in your Render environment variables")
        sys.exit(1)
    
    print("✅ All required environment variables are set")
    
    try:
        # Import and run the scheduler
        from udemypy.scheduler import schedule_bots, TelegramHandler
        
        print("✅ All modules imported successfully")
        print("🤖 Starting bot scheduler...")
        
        # Start the bot with reduced iterations for Render free tier
        schedule_bots(
            bot_handlers=[TelegramHandler()],
            waiting_seconds=60 * 30,  # 30 minutes
            iterations=100,  # Run for 100 iterations (50 hours)
        )
        
    except Exception as e:
        print(f"❌ Bot startup failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main() 