import os
import sys

from flask import Flask, jsonify, request, abort, send_file
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

from fsm import TocMachine
from utils import send_text_message

load_dotenv()

machine = TocMachine(
    states=["start", "song_choices", "help", "chinese_song", "english_song", "japanese_song", "forecast", "dice",
            "dice_predict"],
    transitions=[
        {
            "trigger": "advance",
            "source": "start",
            "dest": "song_choices",
            "conditions": "start_to_song_choices",
        },
        {
            "trigger": "advance",
            "source": "start",
            "dest": "help",
            "conditions": "start_to_help",
        },
        {
            "trigger": "advance",
            "source": "song_choices",
            "dest": "chinese_song",
            "conditions": "song_choices_to_chinese",
        },
        {
            "trigger": "advance",
            "source": "song_choices",
            "dest": "english_song",
            "conditions": "song_choices_to_english",
        },
        {
            "trigger": "advance",
            "source": "song_choices",
            "dest": "japanese_song",
            "conditions": "song_choices_to_japanese",
        },
        {
            "trigger": "advance",
            "source": "chinese_song",
            "dest": "song_choices",
            "conditions": "songs_back_to_choices",
        },
        {
            "trigger": "advance",
            "source": "english_song",
            "dest": "song_choices",
            "conditions": "songs_back_to_choices",
        },
        {
            "trigger": "advance",
            "source": "japanese_song",
            "dest": "song_choices",
            "conditions": "songs_back_to_choices",
        },
        {
            "trigger": "advance",
            "source": "start",
            "dest": "forecast",
            "conditions": "start_to_forecast",
        },
        {
            "trigger": "advance",
            "source": "start",
            "dest": "dice",
            "conditions": "start_to_dice",
        },
        {
            "trigger": "advance",
            "source": "dice",
            "dest": "dice_predict",
            "conditions": "dice_to_dice_predict",
        },
        {
            "trigger": "advance",
            "source": "dice_predict",
            "dest": "dice_predict",
            "conditions": "dice_predict_to_dice_predict",
        },
         {
              "trigger": "advance",
             "source": ["start", "song_choices", "help", "chinese_song", "english_song", "japanese_song", "forecast", "dice", "dice_predict"],
             "dest": "start",
            "conditions": "back_to_menu",
         },
        {"trigger": "go_back",
         "source": ["start", "song_choices", "help", "chinese_song", "english_song", "japanese_song", "forecast",
                    "dice", "dice_predict"],
         "dest": "start"},
    ],
    initial="start",
    auto_transitions=False,
    show_conditions=True,
)

app = Flask(__name__, static_url_path="")

# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv("LINE_CHANNEL_SECRET", None)
channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)
if channel_secret is None:
    print("Specify LINE_CHANNEL_SECRET as environment variable.")
    sys.exit(1)
if channel_access_token is None:
    print("Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.")
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)


@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue

        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=event.message.text)
        )

    return "OK"


@app.route("/webhook", methods=["POST"])
def webhook_handler():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info(f"Request body: {body}")

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue
        if not isinstance(event.message.text, str):
            continue
        print(f"\nFSM STATE: {machine.state}")
        print(f"REQUEST BODY: \n{body}")
        response = machine.advance(event)
        if response == False:
            show_fsm()
            send_text_message(event.reply_token, "不知道做什麼的話 輸入 \"help\" 喔~")

    return "OK"


@app.route("/show-fsm", methods=["GET"])
def show_fsm():
    machine.get_graph().draw("fsm.png", prog="dot", format="png")
    return send_file("fsm.png", mimetype="image/png")


if __name__ == "__main__":
    port = os.environ.get("PORT", 8000)
    app.run(host="0.0.0.0", port=port, debug=True)
