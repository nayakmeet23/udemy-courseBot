#!/usr/bin/env python3
"""
Optimized Render deployment script for UdemyPy Bot
Uses SQLite3 and optimized settings for Render free tier
"""

import os
import sys
import time

def main():
    """Main deployment function with optimized settings"""
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
        # Import and run the scheduler with optimized settings
        from udemypy.scheduler import schedule_bots, TelegramHandler
        
        print("✅ All modules imported successfully")
        print("🤖 Starting optimized bot scheduler...")
        
        # Optimized settings for Render free tier
        waiting_seconds = 60 * 30  # 30 minutes between runs
        iterations = 200  # Run for 200 iterations (100 hours)
        
        print(f"⏰ Bot will run every {waiting_seconds//60} minutes")
        print(f"🔄 Total iterations: {iterations}")
        print(f"⏱️  Total runtime: {iterations * waiting_seconds // 3600} hours")
        
        # Start the bot with optimized settings
        schedule_bots(
            bot_handlers=[TelegramHandler()],
            waiting_seconds=waiting_seconds,
            iterations=iterations,
        )
        
    except KeyboardInterrupt:
        print("\n🛑 Bot stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Bot startup failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main() 