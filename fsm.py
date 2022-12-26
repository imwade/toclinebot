from transitions.extensions import GraphMachine
from utils import send_text_message, send_song_choices_button_message, send_help_button_message, send_forecast_button_message, send_songs_button_message
import random


class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)

    def start_to_song_choices(self, event):
        text = event.message.text
        return text.lower() == "聽歌"

    def on_enter_song_choices(self, event):
        reply_token = event.reply_token
        send_song_choices_button_message(reply_token)

    def start_to_help(self, event):
        text = event.message.text
        return text.lower() == "help"

    def on_enter_help(self, event):
        reply_token = event.reply_token
        send_help_button_message(reply_token)
        self.go_back()

    def song_choices_to_chinese(self, event):
        text = event.message.text
        return text.lower() == "想聽中文歌"

    def on_enter_chinese_song(self, event):
        reply_token = event.reply_token
        link ='https://www.youtube.com/watch?v=kgR5WSGid5Y&list=RDCLAK5uy_n_sz-xNYVBufENsdri7PFhP8ybpfkIlck&start_radio=1'
        send_songs_button_message(reply_token, link)

    def song_choices_to_english(self, event):
        text = event.message.text
        return text.lower() == "想聽英文歌"

    def on_enter_english_song(self, event):
        reply_token = event.reply_token
        link = 'https://www.youtube.com/watch?v=GQAOrCOknCY&list=RDCLAK5uy_mfdqvCAl8wodlx2P2_Ai2gNkiRDAufkkI&start_radio=1'
        send_songs_button_message(reply_token, link)

    def song_choices_to_japanese(self, event):
        text = event.message.text
        return text.lower() == "想聽日文歌"

    def on_enter_japanese_song(self, event):
        reply_token = event.reply_token
        link = 'https://www.youtube.com/watch?v=721FwhVoXpM&list=RDCLAK5uy_nbK9qSkqYZvtMXH1fLCMmC1yn8HEm0W90&start_radio=1'
        send_songs_button_message(reply_token, link)

    def songs_back_to_choices(self, event):
        text = event.message.text
        return text.lower() == "聽其他類型"

    def start_to_forecast(self, event):
        text = event.message.text
        return text.lower() == "天氣預報"

    def on_enter_forecast(self, event):
        reply_token = event.reply_token
        send_forecast_button_message(reply_token)

    def start_to_dice(self, event):
        text = event.message.text
        return text.lower() == "預言"

    def on_enter_dice(self, event):
        reply_token = event.reply_token
        send_text_message(reply_token, '如果想回主選單請輸入: 回主選單\n不然你會陷入預言迴圈裡\n\n 你要預言什麼事情呢?')

    def dice_to_dice_predict(self, event):
        text = event.message.text
        return text != ''

    def dice_predict_to_dice_predict(self, event):
        text = event.message.text
        return text != '回主選單'

    def on_enter_dice_predict(self, event):
        reply_token = event.reply_token
        a = random.randint(0, 100)
        send_text_message(reply_token, '發生機率為：' + str(a) + '%')

    def back_to_menu(self, event):
        text = event.message.text
        if text.lower() == "回主選單":
            reply_token = event.reply_token
            send_help_button_message(reply_token)
        return text.lower() == "回主選單"


