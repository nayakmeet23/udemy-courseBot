#!/bin/bash

# 🚂 Railway Setup Script for Udemy Course Scraper
# This script helps you prepare your project for Railway deployment

echo "🚂 Railway Setup for Udemy Course Scraper"
echo "=========================================="

# Check if we're in the right directory
if [ ! -f "requirements.txt" ]; then
    echo "❌ Error: requirements.txt not found. Please run this script from your project root."
    exit 1
fi

echo "✅ Project structure verified"

# Create .railwayignore if it doesn't exist
if [ ! -f ".railwayignore" ]; then
    echo "📝 Creating .railwayignore file..."
    cat > .railwayignore << EOF
# Ignore files for Railway deployment
udemypy-venv/
venv/
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
env/
pip-log.txt
pip-delete-this-directory.txt
.tox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.log
.git/
.mypy_cache/
.pytest_cache/
.hypothesis/
.env
*.db
*.sqlite
*.sqlite3
reports/
chromedriver-win64/
EOF
    echo "✅ .railwayignore created"
fi

# Check if railway.json exists
if [ ! -f "railway.json" ]; then
    echo "📝 Creating railway.json configuration..."
    cat > railway.json << EOF
{
  "\$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "python -m udemypy.scheduler",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 5
  }
}
EOF
    echo "✅ railway.json created"
fi

# Create a simple health check endpoint
if [ ! -f "health_check.py" ]; then
    echo "📝 Creating health check endpoint..."
    cat > health_check.py << EOF
#!/usr/bin/env python3
"""
Simple health check endpoint for Railway
"""

from flask import Flask, jsonify
import os
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def health_check():
    return jsonify({
        'status': 'healthy',
        'service': 'Udemy Course Scraper',
        'timestamp': datetime.now().isoformat(),
        'environment': os.getenv('RAILWAY_ENVIRONMENT', 'development')
    })

@app.route('/health')
def health():
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
EOF
    echo "✅ health_check.py created"
fi

# Update requirements.txt to include Flask for health check
if ! grep -q "flask" requirements.txt; then
    echo "📝 Adding Flask to requirements.txt for health check..."
    echo "flask==2.3.3" >> requirements.txt
    echo "✅ Flask added to requirements"
fi

echo ""
echo "🎯 Setup Complete!"
echo "=================="
echo ""
echo "Next steps:"
echo "1. Push your code to GitHub:"
echo "   git add ."
echo "   git commit -m 'Add Railway configuration'"
echo "   git push origin main"
echo ""
echo "2. Deploy on Railway:"
echo "   - Go to https://railway.app"
echo "   - Sign up with GitHub"
echo "   - Deploy from your repository"
echo ""
echo "3. Set environment variables in Railway:"
echo "   TOKEN=your_telegram_bot_token"
echo "   CHANNEL_ID=your_channel_id"
echo "   CHANNEL_LINK=your_channel_link"
echo "   GITHUB_LINK=https://github.com/nayakmeet23/udemy-courseBot"
echo "   WHATSAPP_LINK=your_whatsapp_link"
echo "   DATABASE=sqlite3"
echo "   PAGES_TO_SCRAPE=2"
echo "   FAST_MODE=true"
echo "   MAX_COURSES_TO_PROCESS=5"
echo ""
echo "📖 Read RAILWAY_SETUP.md for detailed instructions"
echo ""
echo "🚀 Happy deploying!" 