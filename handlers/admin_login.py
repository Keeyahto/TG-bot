from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
import commands as cmd
from keyboards import Startup_keyboard
from config import config
from keyboards import Admin_keyboard, Moderator_keyboard


async def admin_login(message: types.Message):
    await message.answer("Вход в админ панель выполнен", reply_markup=Admin_keyboard)


async def moderator_login(message: types.Message):
    await message.answer('''Вход в панель модератора выполнен\nПока вы можете «Загрузить курсы»
                            ''', reply_markup=Moderator_keyboard)


def register_handlers_admin_log(dp: Dispatcher):
    dp.register_message_handler(admin_login, is_admin=True,
                                commands=cmd.admin_login_cmd, state=None)
    dp.register_message_handler(moderator_login,
                                is_admin=True,
                                commands=cmd.moderator_login_cmd, state=None)
