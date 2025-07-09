# 🆓 FREE Deployment Options

## Option 1: Railway (Recommended - Easiest)

### Steps:
1. **Go to [Railway.app](https://railway.app)**
2. **Sign up with GitHub** (free)
3. **Click "New Project" → "Deploy from GitHub repo"**
4. **Select your repository**
5. **Set Environment Variables:**
   ```
   TOKEN=your_telegram_bot_token
   CHANNEL_ID=your_channel_id
   CHANNEL_LINK=your_channel_link
   GITHUB_LINK=https://github.com/yourusername/udemypy-project
   WHATSAPP_LINK=https://whatsapp.com/channel/your_channel
   DATABASE=sqlite3
   PAGES_TO_SCRAPE=2
   FAST_MODE=true
   MAX_COURSES_TO_PROCESS=5
   ```
6. **Deploy!**

**Free Tier Limits:**
- 500 hours/month
- 512MB RAM
- Shared CPU

---

## Option 2: Render (Good Alternative)

### Steps:
1. **Go to [Render.com](https://render.com)**
2. **Sign up with GitHub**
3. **Click "New" → "Web Service"**
4. **Connect your repository**
5. **Configure:**
   - **Name:** udemypy-scraper
   - **Environment:** Python
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python -m udemypy.scheduler`
6. **Set Environment Variables** (same as Railway)
7. **Deploy!**

**Free Tier Limits:**
- 750 hours/month
- 512MB RAM
- Sleeps after 15 minutes of inactivity

---

## Option 3: GitHub Actions (Completely Free)

### Steps:
1. **Push your code to GitHub**
2. **Go to your repository → Settings → Secrets and variables → Actions**
3. **Add these secrets:**
   ```
   TOKEN=your_telegram_bot_token
   CHANNEL_ID=your_channel_id
   CHANNEL_LINK=your_channel_link
   GITHUB_LINK=https://github.com/yourusername/udemypy-project
   WHATSAPP_LINK=https://whatsapp.com/channel/your_channel
   ```
4. **The workflow will run automatically every 6 hours**

**Free Tier Limits:**
- 2,000 minutes/month
- Runs on GitHub's servers
- No persistent storage (uses SQLite in memory)

---

## Option 4: PythonAnywhere (Free)

### Steps:
1. **Go to [PythonAnywhere.com](https://www.pythonanywhere.com)**
2. **Sign up for free account**
3. **Upload your code**
4. **Set up a scheduled task:**
   ```bash
   # In PythonAnywhere dashboard
   # Go to Tasks tab
   # Add new task:
   python /home/yourusername/udemypy-project/udemypy/scheduler.py
   # Schedule: Daily at 9 AM
   ```

**Free Tier Limits:**
- 512MB storage
- 1 CPU core
- Limited internet access

---

## 🎯 **Recommended: Railway**

**Why Railway is best:**
- ✅ **Easiest setup**
- ✅ **Good free tier**
- ✅ **Persistent storage**
- ✅ **Automatic restarts**
- ✅ **Good performance**

---

## 📋 **What You Need**

1. **GitHub repository** (push your code)
2. **Telegram bot token** (you have this)
3. **Channel ID** (you have this)
4. **Email address** (for signup)

---

## 🚀 **Quick Start - Railway**

1. **Push your code to GitHub:**
   ```bash
   git add .
   git commit -m "Ready for deployment"
   git push origin main
   ```

2. **Deploy on Railway:**
   - Go to [railway.app](https://railway.app)
   - Sign up with GitHub
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your repository
   - Add environment variables
   - Deploy!

3. **Monitor:**
   - Check logs in Railway dashboard
   - Your bot will run automatically

---

## 💡 **Optimization for Free Tiers**

**Settings to use:**
```bash
PAGES_TO_SCRAPE=2          # Reduce from 3 to 2
FAST_MODE=true             # Enable fast mode
MAX_COURSES_TO_PROCESS=5   # Reduce from 10 to 5
```

**This saves:**
- ⚡ **CPU usage**
- 💾 **Memory usage**
- 🌐 **Network requests**
- ⏱️ **Execution time**

---

## 🔧 **Troubleshooting**

### Railway Issues:
- **Build fails:** Check requirements.txt
- **Runtime errors:** Check logs in Railway dashboard
- **Memory issues:** Reduce PAGES_TO_SCRAPE

### GitHub Actions Issues:
- **Secrets not found:** Check repository secrets
- **Database errors:** SQLite is in-memory, no persistence

### Render Issues:
- **Service sleeps:** Add health check endpoint
- **Build timeout:** Optimize requirements.txt

---

## 📊 **Cost Comparison (All FREE)**

| Platform | Setup Time | Reliability | Storage | Best For |
|----------|------------|-------------|---------|----------|
| **Railway** | 5 min | ⭐⭐⭐⭐⭐ | ✅ | Beginners |
| **Render** | 10 min | ⭐⭐⭐⭐ | ✅ | Intermediate |
| **GitHub Actions** | 15 min | ⭐⭐⭐ | ❌ | Advanced |
| **PythonAnywhere** | 20 min | ⭐⭐ | ✅ | Learning |

**Recommendation: Start with Railway!** 🚀 