import os

from flask import Flask, abort, request
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextMessage, TextSendMessage


app = Flask(__name__)

CHANNEL_SECRET = os.environ['ChannelSecret']
CHANNEL_ACCESS_TOKEN = os.environ['ChannelAccessToken']

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)
    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    text = event.message.text
    if text.lower() == '!id':
        message = f"Your User ID:\n{event.source.user_id}"
        if event.source.type == "group":
            message += f"\n\nYour Group ID:\n{event.source.group_id}"
        reply_token = event.reply_token
        try:
            line_bot_api.reply_message(reply_token, TextSendMessage(text=message))
        except LineBotApiError as e:
            print(f"Line Bot Api Error: {e}")

if __name__ == "__main__":
    app.run()
