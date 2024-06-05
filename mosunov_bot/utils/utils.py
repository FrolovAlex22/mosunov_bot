import logging
import time
import os
import sys
from http import HTTPStatus

import telegram
import requests
from dotenv import load_dotenv


SENDER = os.environ['EMAIL'] # Sender Email/Your Email
PASSWORD = os.environ['PASSWORD'] # Your Email's Password


def send_message(bot, message):
    """Функция для отправки сообщений."""
    logging.debug('Запуск отправки сообщения в Telegram.')
    try:
        bot.send_message(TELEGRAM_CHAT_ID, message)
        logging.debug('Сообщение отправленно в Telegram.')
    except Exception as error:
        message = f'Неудачная попытка отправить сообщение в Telegram{error}'
        logging.error(message)
