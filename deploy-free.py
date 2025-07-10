#!/usr/bin/env python3
"""
Free Deployment Helper for UdemyPy
Helps you choose and deploy to the best free platform
"""

import os
import sys
import webbrowser

# Try to import dotenv, but don't fail if it's not available
try:
    from dotenv import load_dotenv
    DOTENV_AVAILABLE = True
except ImportError:
    DOTENV_AVAILABLE = False
    def load_dotenv():
        pass

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
    
    print("\n2. 🦅 Fly.io (Alternative)")
    print("   ✅ 3 shared-cpu VMs free")
    print("   ✅ No credit card required")
    print("   ✅ Global deployment")
    
    print("\n3. ⚡ GitHub Actions (Completely Free)")
    print("   ✅ 2000 minutes/month free")
    print("   ✅ No credit card required")
    print("   ✅ Runs every 6 hours automatically")
    print("   ⚠️  No persistent storage")
    
    print("\n4. 🚂 Railway (Limited Free)")
    print("   ⚠️  500 hours/month free")
    print("   ⚠️  Requires payment method")
    print("   ✅ Good performance")

def check_environment():
    """Check if environment variables are set"""
    print("\n🔍 Checking environment variables...")
    
    if os.path.exists('.env') and DOTENV_AVAILABLE:
        load_dotenv()
        print("📄 Loaded .env file")
    elif os.path.exists('.env') and not DOTENV_AVAILABLE:
        print("⚠️  .env file found but python-dotenv not installed")
        print("   Environment variables will be read from system only")
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
    print("7. Set environment variables")
    print("8. Deploy!")
    
    choice = input("\n🤔 Open Render in browser? (y/n): ")
    if choice.lower() == 'y':
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
    
    choice = input("\n🤔 Open GitHub repository settings? (y/n): ")
    if choice.lower() == 'y':
        # This would need the actual repo URL
        print("Please go to your GitHub repository manually")

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
    
    choice = input("\n🤔 Install Fly CLI? (y/n): ")
    if choice.lower() == 'y':
        os.system('winget install flyctl')

def main():
    print_banner()
    
    # Check environment first
    if not check_environment():
        print("\n❌ Please set up your environment variables first!")
        print("Create a .env file with your Telegram bot settings.")
        return
    
    # Show options
    show_free_options()
    
    # Get user choice
    print("\n" + "="*50)
    choice = input("🎯 Choose deployment option (1-4): ").strip()
    
    if choice == '1':
        deploy_render()
    elif choice == '2':
        deploy_fly()
    elif choice == '3':
        deploy_github_actions()
    elif choice == '4':
        print("\n🚂 **Railway Free Tier**")
        print("Go to https://railway.app and follow the same steps as Render")
        print("Note: Railway requires a payment method even for free tier")
    else:
        print("❌ Invalid choice. Please select 1-4.")
        return
    
    print("\n🎉 Deployment guide completed!")
    print("📚 Check FREE_DEPLOYMENT.md for detailed instructions")
    print("🔧 Run 'python deploy.py' to test your setup")

if __name__ == "__main__":
    main() 