# ✅ Deployment Checklist

## Pre-Deployment Checklist

### 1. Telegram Bot Setup
- [ ] Created Telegram bot with @BotFather
- [ ] Saved bot token
- [ ] Created Telegram channel
- [ ] Added bot as admin to channel
- [ ] Got channel ID (forward message to @userinfobot)

### 2. Environment Variables
- [ ] `TOKEN` - Your Telegram bot token
- [ ] `CHANNEL_ID` - Your channel ID (e.g., -1001234567890)
- [ ] `CHANNEL_LINK` - Your channel link (e.g., https://t.me/yourchannel)
- [ ] `GITHUB_LINK` - Your GitHub repository link
- [ ] `WHATSAPP_LINK` - Your WhatsApp channel link (optional)

### 3. Code Preparation
- [ ] All code is committed to GitHub
- [ ] No sensitive data in code (tokens, etc.)
- [ ] Requirements.txt is up to date
- [ ] Railway.json is configured

### 4. Testing
- [ ] Run `python deploy.py` to check setup
- [ ] Test locally if possible
- [ ] Verify database connection works

## Deployment Steps

### Railway Deployment
1. [ ] Go to [Railway.app](https://railway.app)
2. [ ] Sign up/Login with GitHub
3. [ ] Click "New Project"
4. [ ] Select "Deploy from GitHub repo"
5. [ ] Connect GitHub account
6. [ ] Select your udemypy-project repository
7. [ ] Wait for automatic detection
8. [ ] Go to Variables tab
9. [ ] Add all environment variables
10. [ ] Wait for deployment to complete
11. [ ] Check logs for any errors

### Post-Deployment Verification
- [ ] Bot is posting courses to Telegram channel
- [ ] No errors in Railway logs
- [ ] Database is working (courses are being saved)
- [ ] Scrapers are finding courses

## Troubleshooting

### If Bot Doesn't Post Courses:
- [ ] Check if bot token is correct
- [ ] Verify bot is admin in channel
- [ ] Check channel ID format (should start with -100)
- [ ] Look at Railway logs for errors

### If Build Fails:
- [ ] Check requirements.txt has all dependencies
- [ ] Verify Python version compatibility
- [ ] Check for syntax errors in code

### If No Courses Found:
- [ ] Increase PAGES_TO_SCRAPE
- [ ] Disable FAST_MODE temporarily
- [ ] Check if scraper sites are accessible
- [ ] Verify internet connectivity

## Monitoring

### Daily Checks:
- [ ] Bot is posting courses regularly
- [ ] No errors in logs
- [ ] Courses are being found and shared

### Weekly Checks:
- [ ] Review scraper performance
- [ ] Check database size
- [ ] Monitor Railway usage/limits

## Cost Management
- [ ] Railway free tier: $5/month (500 hours)
- [ ] Monitor usage in Railway dashboard
- [ ] Consider upgrading if needed

## Success Indicators
✅ Bot posts courses every 30 minutes
✅ No errors in Railway logs
✅ Courses are being found from multiple sources
✅ Database is storing courses properly
✅ Telegram channel is growing with users 