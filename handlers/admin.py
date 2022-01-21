from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import commands as cmd
from keyboards import startup_keyboard


class FDMAdmin(StatesGroup):
    pass
