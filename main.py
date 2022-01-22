from aiogram import Bot, Dispatcher
import asyncio
from aiogram.types.bot_command import BotCommand
from handlers import register_handlers_course, register_handlers_common, register_handlers_upload_course, register_handlers_admin_log
from misc import dp, bot
import commands as cmd


async def set_commands(dp: Dispatcher):
    await dp.bot.set_my_commands([
        BotCommand(command=cmd.start_cmd, description="Общая информация"),
        BotCommand(command=cmd.help_cmd, description="Помощь"),
        BotCommand(command=cmd.cancel_cmd, description='Отмена текущего действия')
    ])


async def main():
    # Регистрация хэндлеров
    register_handlers_common(dp)
    register_handlers_course(dp)
    register_handlers_upload_course(dp)
    register_handlers_admin_log(dp)

    # Установка команд бота
    await set_commands(dp)
    # Запуск поллинга
    # await dp.skip_updates()  # пропуск накопившихся апдейтов (необязательно)
    await dp.start_polling()


if __name__ == '__main__':
    asyncio.run(main())
