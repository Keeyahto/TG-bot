import asyncio

from aiogram import Dispatcher
from aiogram.types.bot_command import BotCommand
from aiogram.utils.executor import start_webhook

import commands as cmd
from handlers import *
from misc import dp, Bot, WEBHOOK_URL, WEBHOOK_PATH, WEBAPP_HOST, WEBAPP_PORT
from models.base import init


# async def on_startup(dp):


async def set_commands(dp: Dispatcher):
    await dp.bot.set_my_commands([
        BotCommand(command=cmd.start_cmd, description="Общая информация"),
        BotCommand(command=cmd.help_cmd, description="Помощь"),
        BotCommand(command=cmd.cancel_cmd, description='Отмена текущего действия')
    ])


async def main(dp):
    # Регистрация хэндлеров
    register_handlers_common(dp)
    register_handlers_course(dp)
    register_handlers_upload_course(dp)
    register_handlers_admin_log(dp)

    # Установка команд бота
    await set_commands(dp)
    # Запуск поллинга
    # await dp.skip_updates()  # пропуск накопившихся апдейтов (необязательно)
    await init()
    await Bot.set_webhook(WEBHOOK_URL, drop_pending_updates=True)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(dp))
    loop.close()
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        skip_updates=True,
        on_startup=main,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )
