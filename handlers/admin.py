from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import commands as cmd
from keyboards import ReplyStartupKeyboard


class FDMAdmin(StatesGroup):
    pass
