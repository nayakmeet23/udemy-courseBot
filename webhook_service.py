from flask import Flask, request
from udemypy.sender.tgm_bot import TelegramBot
from udemypy import settings
from udemypy.database import database
from udemypy.database import settings as db_settings
from udemypy.send_courses import send_courses
from udemypy.scheduler import run_scheduler

app = Flask(__name__)

# Initialize your bot
bot = TelegramBot(
    token=settings.TOKEN,
    channel_id=settings.CHANNEL_ID,
    channel_link=settings.CHANNEL_LINK,
    github_link=settings.GITHUB_LINK,
    whatsapp_link=settings.WHATSAPP_LINK,
    sleep_time_per_course=10,
)
bot.connect()

@app.route('/webhook', methods=['POST'])
def webhook():
    update = request.get_json(force=True)
    print(f"[Webhook] Received update: {update}")

    # If the user sends "/sendcourses", trigger sending to the channel
    if 'message' in update and 'text' in update['message']:
        if update['message']['text'] == '/sendcourses':
            run_scheduler()
    return 'ok'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000) 