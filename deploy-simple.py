#!/usr/bin/env python3
"""
Simple Free Deployment Helper for UdemyPy
No additional dependencies required!
"""

import os
import sys

def print_banner():
    print("🆓" + "="*50)
    print("   UdemyPy FREE Deployment Helper")
    print("="*50)

def show_free_options():
    print("\n🎯 **Best FREE Deployment Options:**")
    print("\n1. 🚀 Render (Recommended)")
    print("   ✅ 750 hours/month free")
    print("   ✅ No credit card required")
    print("   ✅ Easy setup")
    print("   ✅ Automatic deployments")
    
    print("\n2. ⚡ GitHub Actions (Completely Free)")
    print("   ✅ 2000 minutes/month free")
    print("   ✅ No credit card required")
    print("   ✅ Runs every 6 hours automatically")
    print("   ⚠️  No persistent storage")
    
    print("\n3. 🦅 Fly.io (Alternative)")
    print("   ✅ 3 shared-cpu VMs free")
    print("   ✅ No credit card required")
    print("   ✅ Global deployment")

def check_environment():
    """Check if environment variables are set"""
    print("\n🔍 Checking environment variables...")
    
    # Try to load from .env file manually
    if os.path.exists('.env'):
        print("📄 Found .env file - loading variables...")
        try:
            with open('.env', 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        os.environ[key.strip()] = value.strip()
            print("✅ Loaded variables from .env file")
        except Exception as e:
            print(f"⚠️  Could not load .env file: {e}")
    else:
        print("📄 No .env file found - using system environment variables")
    
    required_vars = ['TOKEN', 'CHANNEL_ID', 'CHANNEL_LINK']
    missing = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing.append(var)
    
    if missing:
        print(f"❌ Missing required variables: {', '.join(missing)}")
        print("\n📝 You need to set these in your .env file or environment:")
        for var in missing:
            print(f"   {var}=your_value_here")
        return False
    
    print("✅ All required environment variables are set!")
    return True

def deploy_render():
    """Guide for Render deployment"""
    print("\n🚀 **Deploying to Render (Recommended)**")
    print("\n📋 Steps:")
    print("1. Push your code to GitHub")
    print("2. Go to https://render.com")
    print("3. Sign up with GitHub (no credit card needed)")
    print("4. Click 'New +' → 'Web Service'")
    print("5. Connect your GitHub repository")
    print("6. Configure:")
    print("   - Name: udemypy-bot")
    print("   - Environment: Python 3")
    print("   - Build Command: pip install -r requirements.txt")
    print("   - Start Command: python -m udemypy.scheduler")
    print("   - Plan: Free")
    print("7. Set environment variables:")
    print("   - TOKEN: your_telegram_bot_token")
    print("   - CHANNEL_ID: your_channel_id")
    print("   - CHANNEL_LINK: https://t.me/yourchannel")
    print("   - GITHUB_LINK: https://github.com/yourusername/udemypy-project")
    print("   - WHATSAPP_LINK: https://whatsapp.com/channel/your_channel")
    print("   - PAGES_TO_SCRAPE: 1")
    print("   - FAST_MODE: true")
    print("   - MAX_COURSES_TO_PROCESS: 3")
    print("   - DATABASE: sqlite3")
    print("8. Deploy!")
    
    choice = input("\n🤔 Open Render in browser? (y/n): ")
    if choice.lower() == 'y':
        import webbrowser
        webbrowser.open('https://render.com')

def deploy_github_actions():
    """Guide for GitHub Actions deployment"""
    print("\n⚡ **Deploying with GitHub Actions (Completely Free)**")
    print("\n📋 Steps:")
    print("1. Push your code to GitHub")
    print("2. Go to your repository → Settings → Secrets and variables → Actions")
    print("3. Add these secrets:")
    print("   - TOKEN (your Telegram bot token)")
    print("   - CHANNEL_ID (your channel ID)")
    print("   - CHANNEL_LINK (your channel link)")
    print("   - GITHUB_LINK (your GitHub repo link)")
    print("   - WHATSAPP_LINK (your WhatsApp channel link)")
    print("4. The workflow will run automatically every 6 hours")
    print("5. Check Actions tab to see runs")

def deploy_fly():
    """Guide for Fly.io deployment"""
    print("\n🦅 **Deploying to Fly.io**")
    print("\n📋 Steps:")
    print("1. Install Fly CLI:")
    print("   winget install flyctl")
    print("2. Run: fly launch")
    print("3. Follow the prompts")
    print("4. Set environment variables")
    print("5. Deploy with: fly deploy")

def create_env_template():
    """Create a .env template file"""
    print("\n📝 Creating .env template file...")
    
    env_content = """# Telegram Bot Configuration
TOKEN=your_telegram_bot_token_here
CHANNEL_ID=your_channel_id_here
CHANNEL_LINK=https://t.me/yourchannel

# Social Media Links
GITHUB_LINK=https://github.com/yourusername/udemypy-project
WHATSAPP_LINK=https://whatsapp.com/channel/your_channel

# Scraper Settings (optimized for free tier)
PAGES_TO_SCRAPE=1
FAST_MODE=true
MAX_COURSES_TO_PROCESS=3
MAX_COURSES_TO_SEND=5
DATABASE=sqlite3
"""
    
    try:
        with open('.env.template', 'w') as f:
            f.write(env_content)
        print("✅ Created .env.template file")
        print("📝 Copy .env.template to .env and fill in your values")
    except Exception as e:
        print(f"❌ Could not create .env.template: {e}")

def main():
    print_banner()
    
    # Create .env template if it doesn't exist
    if not os.path.exists('.env.template'):
        create_env_template()
    
    # Check environment first
    if not check_environment():
        print("\n❌ Please set up your environment variables first!")
        print("📝 Create a .env file with your Telegram bot settings:")
        print("   Copy .env.template to .env and fill in your values")
        return
    
    # Show options
    show_free_options()
    
    # Get user choice
    print("\n" + "="*50)
    choice = input("🎯 Choose deployment option (1-3): ").strip()
    
    if choice == '1':
        deploy_render()
    elif choice == '2':
        deploy_github_actions()
    elif choice == '3':
        deploy_fly()
    else:
        print("❌ Invalid choice. Please select 1-3.")
        return
    
    print("\n🎉 Deployment guide completed!")
    print("📚 Check FREE_DEPLOYMENT.md for detailed instructions")

if __name__ == "__main__":
    main() 