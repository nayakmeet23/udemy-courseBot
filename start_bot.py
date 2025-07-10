#!/usr/bin/env python3
"""
Startup script for UdemyPy bot
Handles potential import issues and provides better error reporting
"""

import os
import sys
import traceback

def check_environment():
    """Check if required environment variables are set"""
    required_vars = ['TOKEN', 'CHANNEL_ID', 'CHANNEL_LINK']
    missing = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing.append(var)
    
    if missing:
        print(f"❌ Missing required environment variables: {', '.join(missing)}")
        print("Please set these in your Render environment variables")
        return False
    
    print("✅ All required environment variables are set")
    return True

def main():
    """Main startup function"""
    print("🚀 Starting UdemyPy Bot...")
    
    # Check environment first
    if not check_environment():
        sys.exit(1)
    
    try:
        # Import and run the scheduler
        from udemypy.scheduler import schedule_bots, TelegramHandler
        
        print("✅ All modules imported successfully")
        print("🤖 Starting bot scheduler...")
        
        # Start the bot with reduced iterations for testing
        schedule_bots(
            bot_handlers=[TelegramHandler()],
            waiting_seconds=60 * 30,  # 30 minutes
            iterations=20,  # Run for 20 iterations
        )
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("This might be due to missing dependencies")
        traceback.print_exc()
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
