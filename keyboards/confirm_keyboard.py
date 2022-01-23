from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

import commands as cmd

buttons = ['Нет', 'Да']

ReplyConfirmKeyboard = ReplyKeyboardMarkup(resize_keyboard=True)
ReplyConfirmKeyboard.row(*buttons)

InlineConfirmKeyboard = InlineKeyboardMarkup(row_width=2).row(InlineKeyboardButton(text=buttons[0], callback_data='NO'),
                                                              InlineKeyboardButton(text=buttons[1],
                                                                                   callback_data='YES'))
