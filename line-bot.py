from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
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
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text='你吃飽了嗎'))


if __name__ == "__main__":
    app.run()