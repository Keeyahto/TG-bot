from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
import commands as cmd
from aiogram import types

buttons = ['Нет', 'Да']

Confirm_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
Confirm_keyboard.row(*buttons)
