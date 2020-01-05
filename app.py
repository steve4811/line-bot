from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

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
    msg = event.message.text
    if '圖片' in msg :
        sticker_message = StickerSendMessage(
        package_id='1',
        sticker_id='1'
        )
        line_bot_api.reply_message(
        event.reply_token, sticker_message)
    elif '地址' in msg or '地點' in msg :
        location_message = LocationSendMessage (
            title = '101大樓' ,
            address = '台北市信義路五段7號' ,
            latitude = 25.034207 ,
            longitude = 121.564590
            )
        line_bot_api.reply_message(
        event.reply_token, location_message)
    elif '語言' in msg :
        buttons_template = TemplateSendMessage(
        alt_text='目錄 template',
        template=ButtonsTemplate(
            title='Template-樣板介紹',
            text='Template分為四種，也就是以下四種：',
            actions=[
                MessageTemplateAction(
                    label='Buttons Template',
                    text='Buttons Template'
                ),
                MessageTemplateAction(
                    label='Confirm template',
                    text='Confirm template'
                ),
                MessageTemplateAction(
                    label='Carousel template',
                    text='Carousel template'
                ),
                MessageTemplateAction(
                    label='Image Carousel',
                    text='Image Carousel'
                )
            ]
        )
    )
        line_bot_api.reply_message(event.reply_token, buttons_template)
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