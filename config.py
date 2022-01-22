import os
from telethon import TelegramClient

import logging

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s]%(name)s:%(message)s', level=logging.WARNING)

API_ID: int = int(os.getenv("API_ID"))
API_HASH: str = os.getenv("API_HASH")
BOT_TOKEN: str = os.environ.get("BOT_TOKEN")
STRING_SESSION: str = os.environ.get("STRING_SESSION")


bot = TelegramClient('bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)


