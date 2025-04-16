
from flask import Flask
from threading import Thread
from bot import app as telegram_app

flask_app = Flask(__name__)

@flask_app.route('/')
def home():
    return "Бот работает! ✅"

def run_flask():
    flask_app.run(host='0.0.0.0', port=8080)

def run_telegram():
    telegram_app.run_polling()

if __name__ == "__main__":
    Thread(target=run_flask).start()
    Thread(target=run_telegram).start()
