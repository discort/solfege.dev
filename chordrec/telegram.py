import os

import requests


TELEGRAM_TOKEN = os.environ['TELEGRAM_TOKEN']
TELEGRAM_CHAT_ID = os.environ['TELEGRAM_CHAT_ID']


class TelegramAPI:
    def __init__(self, token, chat_id):
        self.token = token
        self.chat_id = chat_id
        self.url = f"https://api.telegram.org/bot{token}"

    def send_message(self, message):
        payload = {
            'chat_id': self.chat_id,
            'text': message,
            'parse_mode': 'HTML'
        }
        resp = requests.post(
            f"{self.url}/sendMessage",
            data=payload)
        return resp.json()

    def send_audio(self, audio, caption=None):
        if caption is None:
            caption = audio.filename

        payload = {
            'chat_id': TELEGRAM_CHAT_ID,
            'caption': caption,
            'title': audio.filename,
            'parse_mode': 'HTML'
        }
        files = {
            'audio': audio.read(),
        }
        resp = requests.post(
            f"{self.url}/sendAudio",
            data=payload,
            files=files)
        return resp.json()


telegram_api = TelegramAPI(token=TELEGRAM_TOKEN, chat_id=TELEGRAM_CHAT_ID)
