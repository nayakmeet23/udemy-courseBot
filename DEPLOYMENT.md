# 🚀 Deployment Guide

## Option 1: Heroku (Recommended)

### Prerequisites
- Heroku account
- Git installed
- Heroku CLI installed

### Steps:

1. **Install Heroku CLI**
   ```bash
   # Windows
   winget install --id=Heroku.HerokuCLI
   
   # Or download from: https://devcenter.heroku.com/articles/heroku-cli
   ```

2. **Login to Heroku**
   ```bash
   heroku login
   ```

3. **Create Heroku App**
   ```bash
   heroku create your-udemypy-app
   ```

4. **Add PostgreSQL Database**
   ```bash
   heroku addons:create heroku-postgresql:mini
   ```

5. **Set Environment Variables**
   ```bash
   heroku config:set TOKEN=your_telegram_bot_token
   heroku config:set CHANNEL_ID=your_channel_id
   heroku config:set CHANNEL_LINK=your_channel_link
   heroku config:set GITHUB_LINK=https://github.com/yourusername/udemypy-project
   heroku config:set WHATSAPP_LINK=https://whatsapp.com/channel/your_channel
   heroku config:set PAGES_TO_SCRAPE=3
   heroku config:set FAST_MODE=true
   ```

6. **Deploy**
   ```bash
   git add .
   git commit -m "Deploy to Heroku"
   git push heroku main
   ```

7. **Start the Worker**
   ```bash
   heroku ps:scale worker=1
   ```

8. **View Logs**
   ```bash
   heroku logs --tail
   ```

---

## Option 2: Railway

### Steps:

1. **Go to [Railway.app](https://railway.app)**
2. **Connect your GitHub repository**
3. **Set environment variables in Railway dashboard:**
   - `TOKEN`
   - `CHANNEL_ID`
   - `CHANNEL_LINK`
   - `GITHUB_LINK`
   - `WHATSAPP_LINK`
   - `PAGES_TO_SCRAPE`
   - `FAST_MODE`

4. **Deploy automatically**

---

## Option 3: DigitalOcean App Platform

### Steps:

1. **Go to [DigitalOcean App Platform](https://cloud.digitalocean.com/apps)**
2. **Connect your GitHub repository**
3. **Choose Python environment**
4. **Set environment variables**
5. **Deploy**

---

## Option 4: Google Cloud Run

### Steps:

1. **Install Google Cloud CLI**
2. **Build and push Docker image:**
   ```bash
   gcloud builds submit --tag gcr.io/PROJECT_ID/udemypy
   ```
3. **Deploy to Cloud Run:**
   ```bash
   gcloud run deploy udemypy --image gcr.io/PROJECT_ID/udemypy --platform managed
   ```

---

## Environment Variables Required

```bash
# Telegram Bot
TOKEN=your_telegram_bot_token
CHANNEL_ID=your_channel_id
CHANNEL_LINK=your_channel_link

# Links
GITHUB_LINK=https://github.com/yourusername/udemypy-project
WHATSAPP_LINK=https://whatsapp.com/channel/your_channel

# Scraper Settings
PAGES_TO_SCRAPE=3
FAST_MODE=true
MAX_COURSES_TO_PROCESS=10

# Database (Auto-set by Heroku)
DATABASE_URL=postgresql://...
```

---

## Monitoring & Maintenance

### View Logs
```bash
# Heroku
heroku logs --tail

# Railway
railway logs

# DigitalOcean
doctl apps logs your-app-id
```

### Restart Service
```bash
# Heroku
heroku restart

# Railway
railway service restart
```

### Update Code
```bash
git add .
git commit -m "Update"
git push heroku main  # or your platform
```

---

## Cost Estimation

- **Heroku**: $7/month (basic dyno) + $5/month (PostgreSQL mini)
- **Railway**: $5/month (pro plan)
- **DigitalOcean**: $5/month (basic app)
- **Google Cloud Run**: Pay per use (~$1-5/month)

---

## Troubleshooting

### Common Issues:

1. **Database Connection Error**
   - Check `DATABASE_URL` environment variable
   - Ensure database is provisioned

2. **Telegram Bot Not Working**
   - Verify bot token is correct
   - Check if bot is admin in channel
   - Verify channel ID format

3. **Scraper Not Finding Courses**
   - Check internet connectivity
   - Verify scraper sites are accessible
   - Check rate limiting

4. **Memory Issues**
   - Reduce `PAGES_TO_SCRAPE`
   - Enable `FAST_MODE=true`
   - Reduce `MAX_COURSES_TO_PROCESS` 