from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

import commands as cmd
from keyboards import Startup_keyboard


async def start(message: types.Message, state: FSMContext):
    await message.answer(
        "Добро пожаловать! Здесь можно купить вебинары ЕГЭ по нужным тебе предметам.",
        reply_markup=Startup_keyboard)


async def help(message: types.Message, state: FSMContext):
    await message.answer(
        '''Что умеет бот и как им пользоваться?\n
        «Купить курс»''',
    )


async def cancel(message: types.Message, state: FSMContext) -> None:
    """
    Allow user to cancel any action
    """
    await state.finish()
    await message.answer(
        "Действие отменено",
        reply_markup=Startup_keyboard,
    )

async def test(message: types.Message, state: FSMContext) -> None:
    await message.answer(message.html_text, parse_mode='HTML')


def register_handlers_common(dp: Dispatcher):
    dp.register_message_handler(start, commands=cmd.start_cmd, state=None)
    dp.register_message_handler(help, commands=cmd.help_cmd, state=None)
    dp.register_message_handler(cancel, commands=cmd.cancel_cmd, state="*")
    dp.register_message_handler(cancel, Text(equals=cmd.cancel_cmd, ignore_case=True), state="*")



