import os
import sys
import tempfile
from argparse import ArgumentParser

from flask import Flask, abort, request
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import (AudioMessage, BeaconEvent, BoxComponent,
                            BubbleContainer, ButtonComponent, ButtonsTemplate,
                            CameraAction, CameraRollAction, CarouselColumn,
                            CarouselTemplate, ConfirmTemplate,
                            DatetimePickerAction, FileMessage, FlexSendMessage,
                            FollowEvent, IconComponent, ImageCarouselColumn,
                            ImageCarouselTemplate, ImageComponent,
                            ImageMessage, ImageSendMessage, JoinEvent,
                            LeaveEvent, LocationAction, LocationMessage,
                            LocationSendMessage, MessageAction, MessageEvent,
                            PostbackAction, PostbackEvent, QuickReply,
                            QuickReplyButton, SeparatorComponent, SourceGroup,
                            SourceRoom, SourceUser, SpacerComponent,
                            StickerMessage, StickerSendMessage,
                            TemplateSendMessage, TextComponent, TextMessage,
                            TextSendMessage, UnfollowEvent, URIAction,
                            VideoMessage)

app = Flask(__name__)

CHANNEL_SECRET = os.environ['ChannelSecret']
CHANNEL_ACCESS_TOKEN = os.environ['ChannelAccessToken']

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)


@app.route('/')
def hello_server():
    return "Hello, World !"


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)

    # handle webhook body
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
            line_bot_api.reply_message(
                reply_token, TextSendMessage(text=message))
        except LineBotApiError as e:
            print(f"Line Bot Api Error: {e}")

if __name__ == "__main__":
    arg_parser = ArgumentParser(
        usage='Usage: python ' + __file__ + ' [--port <port>] [--help]'
    )
    arg_parser.add_argument('-p', '--port', type=int,
                            default=8000, help='port')
    arg_parser.add_argument('-d', '--debug', default=True, help='debug')
    options = arg_parser.parse_args()

    app.run(debug=options.debug, port=options.port)
