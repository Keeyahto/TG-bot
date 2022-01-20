from aiogram import Bot
import asyncio
from aiogram.types.bot_command import BotCommand
from handlers.choose_course import register_handlers_course
from handlers.common import register_handlers_common
from misc import dp, bot

async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/course", description="Купить курс"),
        BotCommand(command="/cancel", description="Отменить текущее действие")
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
