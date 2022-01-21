from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
import commands as cmd
from keyboards import startup_keyboard


async def start(message: types.Message, state: FSMContext):
    await message.answer(
        "Добро пожаловать! Здесь можно купить вебинары ЕГЭ по нужным тебе предметам.",
        reply_markup=startup_keyboard)


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
        reply_markup=types.ReplyKeyboardRemove(),
    )


def register_handlers_common(dp: Dispatcher):
    dp.register_message_handler(start, commands=cmd.start_cmd)
    dp.register_message_handler(help, commands=cmd.help_cmd)
    dp.register_message_handler(cancel, commands=cmd.cancel_cmd, state="*")
