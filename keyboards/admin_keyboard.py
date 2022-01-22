from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
import commands as cmd
from aiogram import types

buttons = ['']

Admin_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
Admin_keyboard.row(*buttons)
