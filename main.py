import asyncio

from aiogram import Dispatcher
from aiogram.types.bot_command import BotCommand
from aiogram.utils.executor import start_webhook

import commands as cmd
from handlers import *
from is_webhook_method import webhook_method
from misc import dp, bot, WEBHOOK_URL, WEBHOOK_PATH, WEBAPP_HOST, WEBAPP_PORT
from models.base import init


async def set_commands(dp: Dispatcher):
    await dp.bot.set_my_commands([
        BotCommand(command=cmd.start_cmd, description="Общая информация"),
        BotCommand(command=cmd.help_cmd, description="Помощь"),
        BotCommand(command=cmd.cancel_cmd, description='Отмена текущего действия')
    ])


async def on_shutdown(dp):
    await bot.delete_webhook()
    await dp.storage.close()
    await dp.storage.wait_closed()


async def on_startup(dp, webhook=True):
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
    if webhook:
        await bot.set_webhook(WEBHOOK_URL, drop_pending_updates=True)


async def no_webhook_main():
    await on_startup(dp, webhook=False)
    await dp.start_polling()


def main():
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        skip_updates=True,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )


if __name__ == '__main__':
    if webhook_method:
        main()
    else:
        asyncio.run(no_webhook_main())
