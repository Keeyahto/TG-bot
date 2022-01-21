from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
import commands as cmd
from aiogram import types

buttons = ['Нет', 'Да']

confirm_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
confirm_keyboard.row(*buttons)
