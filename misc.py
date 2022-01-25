import os

from aiogram import Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher

from config import config
from filters import AdminFilter
from is_webhook_method import webhook_method

storage = MemoryStorage()

# Heroku settings
HEROKU_APP_NAME = config['GENERAL']['HEROKU_APP_NAME']
WEBHOOK_HOST = f'https://{HEROKU_APP_NAME}.herokuapp.com'
WEBHOOK_PATH = f'/webhook/{config["GENERAL"]["TELEGRAM_TOKEN"]}'
WEBHOOK_URL = f'{WEBHOOK_HOST}{WEBHOOK_PATH}'
WEBAPP_HOST = '0.0.0.0'

try:
    WEBAPP_PORT = int(os.getenv("PORT"))
except TypeError:
    WEBAPP_PORT = 5000

token = config['GENERAL']['TELEGRAM_TOKEN'] if webhook_method else config['GENERAL']['TELEGRAM_TOKEN_TEST']
bot = Bot(token=token)
dp = Dispatcher(bot, storage=storage)
dp.filters_factory.bind(AdminFilter)
