from aiogram import Bot
import asyncio
from aiogram.types.bot_command import BotCommand
from handlers import register_handlers_course, register_handlers_common
from misc import dp, bot
import commands as cmd
async def set_commands(bot: Bot):
    commands = [
        BotCommand(command=cmd.start_cmd, description="Общая информация"),
        BotCommand(command=cmd.help_cmd, description="Помощь")
    ]
    await bot.set_my_commands(commands)
async def main():
    # Регистрация хэндлеров
    register_handlers_course(dp)
    register_handlers_common(dp)

    # Установка команд бота
    await set_commands(bot)

    # Запуск поллинга
    # await dp.skip_updates()  # пропуск накопившихся апдейтов (необязательно)
    await dp.start_polling()



if __name__ == '__main__':
    asyncio.run(main())
