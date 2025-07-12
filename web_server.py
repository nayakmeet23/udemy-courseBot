#!/usr/bin/env python3
"""
Simple web server for UdemyPy bot
Runs the bot in background while serving health check endpoints
"""

from flask import Flask, jsonify
import threading
import os
import time
from datetime import datetime

# Import the bot scheduler
from udemypy.scheduler import schedule_bots, TelegramHandler

app = Flask(__name__)

# Global variables to track bot status
bot_status = {
    "running": False,
    "started_at": None,
    "iterations_completed": 0,
    "last_activity": None,
    "error": None
}

def run_bot():
    """Run the bot in background thread"""
    global bot_status
    
    try:
        bot_status["running"] = True
        bot_status["started_at"] = datetime.now().isoformat()
        bot_status["error"] = None
        
        print("[Web Server] Starting bot in background...")
        
        # Run bot with reduced iterations for free tier
        schedule_bots(
            bot_handlers=[TelegramHandler()],
            waiting_seconds=60 * 30,  # 30 minutes
            iterations=5,  # Reduced for free tier
        )
        
    except Exception as e:
        bot_status["error"] = str(e)
        bot_status["running"] = False
        print(f"[Web Server] Bot error: {e}")

@app.route('/')
def home():
    """Home page with bot status"""
    return jsonify({
        "service": "UdemyPy Bot",
        "status": "running",
        "bot_status": bot_status,
        "endpoints": {
            "health": "/health",
            "status": "/status",
            "start": "/start",
            "stop": "/stop"
        }
    })

@app.route('/health')
def health():
    """Health check endpoint for Render"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "bot_running": bot_status["running"]
    })

@app.route('/status')
def status():
    """Detailed bot status"""
    return jsonify(bot_status)

@app.route('/start')
def start_bot():
    """Start the bot manually"""
    if bot_status["running"]:
        return jsonify({"message": "Bot is already running", "status": bot_status})
    
    # Start bot in background thread
    bot_thread = threading.Thread(target=run_bot, daemon=True)
    bot_thread.start()
    
    return jsonify({
        "message": "Bot started successfully",
        "status": "starting"
    })

@app.route('/stop')
def stop_bot():
    """Stop the bot (not implemented for simplicity)"""
    return jsonify({
        "message": "Bot stop not implemented. Restart the service to stop.",
        "status": "running"
    })

def start_web_server():
    """Start the Flask web server"""
    port = int(os.environ.get('PORT', 10000))
    
    # Start bot automatically when server starts
    print("[Web Server] Starting bot automatically...")
    bot_thread = threading.Thread(target=run_bot, daemon=True)
    bot_thread.start()
    
    print(f"[Web Server] Starting Flask server on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)

if __name__ == "__main__":
    start_web_server() 