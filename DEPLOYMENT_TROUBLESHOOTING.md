# 🔧 Deployment Troubleshooting Guide

## 🚨 **Common Render Deployment Errors & Solutions**

### **Error 1: ModuleNotFoundError: No module named 'dotenv'**

**Solution:**
- ✅ Fixed in latest code - using `requirements-deploy.txt`
- ✅ Settings.py now handles missing dotenv gracefully
- ✅ Using startup script for better error handling

### **Error 2: Environment Variables Not Found**

**Solution:**
1. **In Render Dashboard:**
   - Go to your service → Environment
   - Add these variables:
   ```
   TOKEN=your_telegram_bot_token
   CHANNEL_ID=your_channel_id
   CHANNEL_LINK=https://t.me/yourchannel
   GITHUB_LINK=https://github.com/yourusername/udemypy-project
   WHATSAPP_LINK=https://whatsapp.com/channel/your_channel
   PAGES_TO_SCRAPE=1
   FAST_MODE=true
   MAX_COURSES_TO_PROCESS=3
   DATABASE=sqlite3
   ```

### **Error 3: Build Fails**

**Solution:**
- ✅ Using `requirements-deploy.txt` with exact versions
- ✅ Upgraded pip in build command
- ✅ Using startup script for better error reporting

### **Error 4: Bot Not Starting**

**Solution:**
- ✅ Created `start_bot.py` with comprehensive error handling
- ✅ Better logging and error messages
- ✅ Environment variable validation

---

## 🛠️ **Step-by-Step Fix Process**

### **Step 1: Update Your Code**
```bash
git add .
git commit -m "Fix deployment issues"
git push origin main
```

### **Step 2: Check Render Configuration**
1. **Go to Render Dashboard**
2. **Select your service**
3. **Check Environment Variables** (all required ones should be set)
4. **Check Build Command:** `pip install -r requirements-deploy.txt`
5. **Check Start Command:** `python start_bot.py`

### **Step 3: Monitor Deployment**
1. **Watch the build logs**
2. **Look for any error messages**
3. **Check if all dependencies install correctly**

---

## 📋 **Required Environment Variables**

Make sure these are set in Render:

| Variable | Description | Example |
|----------|-------------|---------|
| `TOKEN` | Telegram bot token | `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz` |
| `CHANNEL_ID` | Telegram channel ID | `-1001234567890` |
| `CHANNEL_LINK` | Channel link | `https://t.me/yourchannel` |
| `GITHUB_LINK` | Your GitHub repo | `https://github.com/yourusername/udemypy-project` |
| `WHATSAPP_LINK` | WhatsApp channel | `https://whatsapp.com/channel/your_channel` |
| `PAGES_TO_SCRAPE` | Number of pages | `1` |
| `FAST_MODE` | Enable fast mode | `true` |
| `MAX_COURSES_TO_PROCESS` | Max courses | `3` |
| `DATABASE` | Database type | `sqlite3` |

---

## 🔍 **Debugging Steps**

### **1. Check Build Logs**
- Look for dependency installation errors
- Check if all packages install correctly
- Verify Python version compatibility

### **2. Check Runtime Logs**
- Look for import errors
- Check environment variable loading
- Verify database connection

### **3. Test Locally First**
```bash
python test_deployment.py
python start_bot.py
```

---

## 🎯 **Success Indicators**

✅ **Build completes without errors**
✅ **All dependencies install correctly**
✅ **Environment variables load properly**
✅ **Database connects successfully**
✅ **Bot starts and connects to Telegram**
✅ **Courses are found and posted**

---

## 🆘 **Still Having Issues?**

### **Option 1: Use GitHub Actions (Completely Free)**
- No deployment issues
- Runs every 6 hours automatically
- No environment setup required

### **Option 2: Try Fly.io**
- Alternative free platform
- Different deployment method
- Often more reliable

### **Option 3: Check Render Status**
- Visit [render.com/status](https://render.com/status)
- Check if Render is having issues

---

## 📞 **Get Help**

1. **Check the logs** in Render dashboard
2. **Run local tests** with `python test_deployment.py`
3. **Verify environment variables** are set correctly
4. **Try the startup script** locally: `python start_bot.py`

---

## 🎉 **Expected Success Flow**

1. **Code pushes to GitHub** ✅
2. **Render detects changes** ✅
3. **Build starts** ✅
4. **Dependencies install** ✅
5. **Bot starts** ✅
6. **Connects to Telegram** ✅
7. **Finds and posts courses** ✅
8. **Runs continuously** ✅ 