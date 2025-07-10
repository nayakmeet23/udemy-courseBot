# 🆓 Free Deployment Guide - Lifetime Free

## 🎯 **Best Free Options (No Credit Card Required)**

### **1. Render (Recommended)**
- ✅ **750 hours/month free** (enough for 24/7 bot)
- ✅ **No credit card required**
- ✅ **Automatic deployments**
- ✅ **Easy setup**

### **2. Fly.io (Alternative)**
- ✅ **3 shared-cpu VMs free**
- ✅ **No credit card required for basic tier**
- ✅ **Global deployment**

### **3. Railway Free Tier**
- ⚠️ **500 hours/month** (limited but free)
- ⚠️ **Requires payment method**

---

## 🚀 **Option 1: Render (Recommended)**

### Step 1: Prepare Your Code
1. **Push your code to GitHub**
2. **Ensure render.yaml is in your repo** (already done)

### Step 2: Deploy to Render
1. **Go to [Render.com](https://render.com)**
2. **Sign up with GitHub** (no credit card needed)
3. **Click "New +" → "Web Service"**
4. **Connect your GitHub repository**
5. **Select your udemypy-project repo**
6. **Configure the service:**
   - **Name**: `udemypy-bot`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python -m udemypy.scheduler`
   - **Plan**: `Free`

### Step 3: Set Environment Variables
In Render dashboard, go to Environment → Environment Variables and add:

```bash
# Required
TOKEN=your_telegram_bot_token
CHANNEL_ID=your_channel_id
CHANNEL_LINK=https://t.me/yourchannel

# Optional (with free-friendly defaults)
GITHUB_LINK=https://github.com/yourusername/udemypy-project
WHATSAPP_LINK=https://whatsapp.com/channel/your_channel
PAGES_TO_SCRAPE=1
FAST_MODE=true
MAX_COURSES_TO_PROCESS=3
MAX_COURSES_TO_SEND=5
DATABASE=sqlite3
PYTHONUNBUFFERED=1
```

### Step 4: Deploy
1. **Click "Create Web Service"**
2. **Wait for build to complete**
3. **Check logs for any errors**

---

## 🚀 **Option 2: Fly.io (Alternative)**

### Step 1: Install Fly CLI
```bash
# Windows
winget install flyctl

# Or download from: https://fly.io/docs/hands-on/install-flyctl/
```

### Step 2: Create fly.toml
```bash
fly launch
```

### Step 3: Deploy
```bash
fly deploy
```

---

## 🚀 **Option 3: Railway Free Tier**

### Step 1: Deploy to Railway
1. **Go to [Railway.app](https://railway.app)**
2. **Sign up with GitHub**
3. **Create new project**
4. **Connect your repository**
5. **Set environment variables**
6. **Deploy**

### Step 2: Monitor Usage
- **Free tier**: 500 hours/month
- **Monitor in Railway dashboard**
- **Bot will auto-sleep when limit reached**

---

## ⚙️ **Free Tier Optimizations**

### **Reduced Resource Usage:**
- `PAGES_TO_SCRAPE=1` (instead of 2-3)
- `MAX_COURSES_TO_PROCESS=3` (instead of 10)
- `MAX_COURSES_TO_SEND=5` (instead of 10)
- `FAST_MODE=true` (enabled)

### **Memory Optimizations:**
- Using SQLite instead of MySQL
- Reduced concurrent requests
- Faster processing times

### **Cost-Saving Features:**
- Bot runs every 30 minutes (not continuously)
- Efficient scraping with retry logic
- Minimal database operations

---

## 📊 **Free Tier Limits Comparison**

| Platform | Free Hours/Month | Credit Card | Best For |
|----------|------------------|-------------|----------|
| **Render** | 750 | ❌ No | ✅ Best choice |
| **Fly.io** | Unlimited | ❌ No | ✅ Good alternative |
| **Railway** | 500 | ⚠️ Yes | ⚠️ Limited but works |

---

## 🔧 **Troubleshooting Free Tier Issues**

### **Render Free Tier:**
- **Service sleeps after 15 minutes of inactivity**
- **Bot will wake up when new requests come**
- **750 hours = ~31 days (enough for 24/7)**

### **Railway Free Tier:**
- **500 hours = ~20 days**
- **Service stops when limit reached**
- **Upgrade to paid plan if needed**

### **Fly.io Free Tier:**
- **3 shared-cpu VMs**
- **3GB persistent volume**
- **Global deployment**

---

## 💡 **Tips for Free Deployment**

1. **Start with Render** - easiest and most generous
2. **Use optimized settings** (already configured)
3. **Monitor usage** in platform dashboard
4. **Have backup plan** (Fly.io) ready
5. **Test thoroughly** before going live

---

## 🎉 **Success Indicators**

✅ Bot posts courses every 30 minutes
✅ No errors in platform logs
✅ Courses found from multiple sources
✅ Database working properly
✅ Free tier limits not exceeded
✅ No unexpected charges

---

## 📞 **Need Help?**

- **Render Support**: [render.com/docs](https://render.com/docs)
- **Fly.io Support**: [fly.io/docs](https://fly.io/docs)
- **Railway Support**: [railway.app/docs](https://railway.app/docs) 