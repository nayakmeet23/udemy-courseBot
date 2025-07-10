# 🚀 Quick Deployment Guide - Railway

## Prerequisites
- GitHub account
- Railway account (free at railway.app)
- Telegram bot token and channel setup

## Step 1: Set Up Telegram Bot

1. **Create a Telegram Bot:**
   - Message @BotFather on Telegram
   - Send `/newbot`
   - Follow instructions to create your bot
   - Save the bot token

2. **Create a Telegram Channel:**
   - Create a new channel in Telegram
   - Add your bot as an admin
   - Get the channel ID (forward a message to @userinfobot)

## Step 2: Deploy to Railway

1. **Go to [Railway.app](https://railway.app)**
2. **Sign up/Login with GitHub**
3. **Click "New Project"**
4. **Select "Deploy from GitHub repo"**
5. **Connect your GitHub account**
6. **Select your udemypy-project repository**
7. **Railway will automatically detect it's a Python project**

## Step 3: Configure Environment Variables

In Railway dashboard, go to your project → Variables tab and add:

```bash
# Required Telegram Settings
TOKEN=your_telegram_bot_token_here
CHANNEL_ID=your_channel_id_here
CHANNEL_LINK=https://t.me/your_channel_username

# Social Media Links
GITHUB_LINK=https://github.com/yourusername/udemypy-project
WHATSAPP_LINK=https://whatsapp.com/channel/your_channel_here

# Scraper Settings
PAGES_TO_SCRAPE=2
FAST_MODE=true
MAX_COURSES_TO_PROCESS=5
MAX_COURSES_TO_SEND=10

# Database Settings
DATABASE=sqlite3
```

## Step 4: Deploy

1. **Railway will automatically deploy your app**
2. **Wait for build to complete**
3. **Check the logs to ensure everything is working**

## Step 5: Monitor Your Bot

1. **Go to your Telegram channel**
2. **You should see courses being posted automatically**
3. **Check Railway logs if there are issues**

## Troubleshooting

### Common Issues:

1. **Bot not posting courses:**
   - Check if bot token is correct
   - Verify bot is admin in channel
   - Check Railway logs for errors

2. **Build fails:**
   - Ensure all dependencies are in requirements.txt
   - Check Python version compatibility

3. **No courses found:**
   - Increase PAGES_TO_SCRAPE
   - Check if scraper sites are accessible
   - Disable FAST_MODE temporarily

## Cost
- Railway free tier: $5/month (includes 500 hours)
- Perfect for this type of bot

## Next Steps
- Monitor your bot performance
- Adjust scraper settings as needed
- Consider upgrading for more resources 