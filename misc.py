import os

from aiogram import Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher

from config import config
from filters import AdminFilter

storage = MemoryStorage()

HEROKU_APP_NAME = config['GENERAL']['HEROKU_APP_NAME']

# webhook settings
WEBHOOK_HOST = f'https://{HEROKU_APP_NAME}.herokuapp.com'
WEBHOOK_PATH = f'/webhook/{config["GENERAL"]["TELEGRAM_TOKEN"]}'
WEBHOOK_URL = f'{WEBHOOK_HOST}{WEBHOOK_PATH}'

# webserver settings
WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = int(os.getenv("PORT"))

bot = Bot(token=config['GENERAL']['TELEGRAM_TOKEN'])
dp = Dispatcher(bot, storage=storage)
dp.filters_factory.bind(AdminFilter)
