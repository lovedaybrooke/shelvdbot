import re
import os

from flask import Flask, request
import telegram
import requests


token = os.environ['TELEGRAM_TOKEN']
bot = telegram.Bot(token=token)

app = Flask(__name__)


@app.route('/{}'.format(token), methods=['POST'])
def respond():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    chat_id = update.message.chat.id
    msg_id = update.message.message_id

    if str(chat_id) == os.environ['CHAT_ID']:
        text = update.message.text.encode('utf-8').decode().lower()

        try:
            response_message = requests.post(
                    'http://shelvd.katmatfield.com/webhook',
                    data={
                        'From': int(os.environ['RECIPIENT_NUMBER']),
                        'Text': text
                    }).text
            bot.sendMessage(chat_id=chat_id, text=response_message,
                            reply_to_message_id=msg_id)

        except Exception:
            bot.sendMessage(chat_id=chat_id,
                            text="Bof! Something went wrong",
                            reply_to_message_id=msg_id)

        return 'ok'
    else:
        bot.sendMessage(chat_id=chat_id,
                        text="This bot is not for you. Sorry!")
        return 'ok'


@app.route('/setwebhook', methods=['GET', 'POST'])
def set_webhook():
    s = bot.setWebhook('https://shelvd-bot.herokuapp.com/{HOOK}'.format(
                       HOOK=token))
    if s:
        return "webhook setup ok"
    else:
        return "webhook setup failed"


if __name__ == '__main__':
    app.run(threaded=True)
