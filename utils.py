import os

from linebot import LineBotApi, WebhookParser
from linebot.models import MessageEvent, TextMessage, TextSendMessage, PostbackAction, URIAction, MessageAction, \
    TemplateSendMessage, ButtonsTemplate

channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)


def send_text_message(reply_token, text):
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.reply_message(reply_token, TextSendMessage(text=text))

    return "OK"


def send_song_choices_button_message(reply_token):
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.reply_message(reply_token, TemplateSendMessage(
        alt_text='歌曲類型',
        template=ButtonsTemplate(
            thumbnail_image_url='https://i.imgur.com/61W7iV3.png',
            title='想選什麼類型的歌',
            text='請選擇~',
            actions=[
                MessageAction(
                    label='英文歌',
                    text='想聽英文歌'
                ),
                MessageAction(
                    label='中文歌',
                    text='想聽中文歌'
                ),
                MessageAction(
                    label='日文歌',
                    text='想聽日文歌'
                ),
                MessageAction(
                    label='返回',
                    text='回主選單'
                )
            ]
        )
    ))

    return "OK"


def send_songs_button_message(reply_token, link):
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.reply_message(reply_token, TemplateSendMessage(
        alt_text='聽歌吧',
        template=ButtonsTemplate(
            thumbnail_image_url='https://i.imgur.com/IHc6HjJ.jpg',
            title=' ',
            text='請選擇~',
            actions=[
                URIAction(
                    label='聽歌！',
                    uri=link
                ),
                MessageAction(
                    label='返回',
                    text='聽其他類型'
                ),
                MessageAction(
                    label='回主選單',
                    text='回主選單'
                )
            ]
        )
    ))

    return "OK"


def send_help_button_message(reply_token):
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.reply_message(reply_token, TemplateSendMessage(
        alt_text='功能選項',
        template=ButtonsTemplate(
            thumbnail_image_url='https://i.imgur.com/j0LMfg5.jpg',
            title='早安你好',
            text='要做什麼呢',
            actions=[
                MessageAction(
                    label='聽歌',
                    text='聽歌'
                ),
                MessageAction(
                    label='天氣預報',
                    text='天氣預報'
                ),
                MessageAction(
                    label='預言',
                    text='預言'
                )
            ]
        )
    ))

    return "OK"


def send_forecast_button_message(reply_token):
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.reply_message(reply_token, TemplateSendMessage(
        alt_text='功能選項',
        template=ButtonsTemplate(
            thumbnail_image_url='https://i.imgur.com/gkke6VW.jpg',
            title='早安你好',
            text='各種氣象喔',
            actions=[
                URIAction(
                    label='天氣狀況',
                    uri='https://www.cwb.gov.tw/V8/C/W/OBS_Map.html'
                ),
                URIAction(
                    label='地震網站',
                    uri='https://www.cwb.gov.tw/V8/C/E/index.html'
                ),
                MessageAction(
                    label='回主選單',
                    text='回主選單'
                )
            ]
        )
    ))

    return "OK"


"""
def send_image_url(id, img_url):
    pass

def send_button_message(id, text, buttons):
line_bot_api = LineBotApi('你的 Channel access token')
line_bot_api.push_message('你的 user ID', TemplateSendMessage(
    alt_text='ButtonsTemplate',
    template=ButtonsTemplate(
        thumbnail_image_url='https://steam.oxxostudio.tw/download/python/line-template-message-demo.jpg',
        title='OXXO.STUDIO',
        text='這是按鈕樣板',
        actions=[
            PostbackAction(
                label='postback',
                data='發送 postback'
            ),
            MessageAction(
                label='說 hello',
                text='hello'
            ),
            URIAction(
                label='前往 STEAM 教育學習網',
                uri='https://steam.oxxostudio.tw'
            )
        ]
    )
))
    pass
"""
