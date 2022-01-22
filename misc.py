from config import config
from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from filters import AdminFilter
storage = MemoryStorage()

bot = Bot(token=config['GENERAL']['TELEGRAM_TOKEN'])
dp = Dispatcher(bot, storage=storage)
dp.filters_factory.bind(AdminFilter)
