from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

import commands as cmd

ReplyDontUpload = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(KeyboardButton('/stop'))
ReplyModeratorKeyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
ReplyModeratorKeyboard.add(KeyboardButton(cmd.upload_course_cmd))
InlineModeratorKeyboard = InlineKeyboardMarkup(row_width=2)
InlineModeratorKeyboard.add(InlineKeyboardButton(text=cmd.upload_course_cmd, callback_data=cmd.upload_course_cmd))


