from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,ImageSendMessage
)

app = Flask(__name__)

line_bot_api = LineBotApi('6pDlBsZ14xoSj5tdWnoVMB6bTs6lxc6I34lYt3MyHZgp6BI7uxi4LifbUmMtUH2slyN5YS9yd3JQRy7c1DDsXA84/G59LLA6f/MixWvjAgdHdEZMOxGpi6rY1dbeM2PuPoUkYa6gZR2lACpxwU0QqAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('2f49c6713ac7da6dda6da6e6d4d45b3f')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    image_message = ImageSendMessage(
    original_content_url='https://line-bot-1231.herokuapp.com/callback/pasta.png',
    preview_image_url='https://line-bot-1231.herokuapp.com/callback/pasta.png'
    )
    msg = event.message.text
    if '圖片' in msg :
        line_bot_api.reply_message(
        event.reply_token, image_message)
        return 

    if msg in ['hi' ,'Hi' ,'HI' ,'嗨'] :
        r = '嗨'
    elif msg == '你是誰' :
        r = '我是機器人'
    elif '訂位' in msg :
        r = '請撥訂位電話 3388'
    else :
        r = '你說什麼'

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=r))


if __name__ == "__main__":
    app.run()