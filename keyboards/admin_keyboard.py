from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
import commands as cmd
from aiogram import types

buttons = ['']

ReplyAdminKeyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
ReplyAdminKeyboard.row(*buttons)
