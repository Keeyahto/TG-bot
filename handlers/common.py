from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


async def cmd_start(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(
        "Привет! Тут ты можешь купить курсы для подготовки к ЕГЭ.",
    )

async def cmd_cancel(message: types.Message, state: FSMContext) -> None:
    """
    Allow user to cancel any action
    """
    await state.finish()
    await message.answer(
        "Cancelled.",
        reply_markup=types.ReplyKeyboardRemove(),
    )

def register_handlers_common(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands="start", state="*")
    dp.register_message_handler(cmd_cancel, commands="cancel", state="*")
