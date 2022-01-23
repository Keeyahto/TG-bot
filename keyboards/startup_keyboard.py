from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import commands as cmd

ReplyStartupKeyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=2)
ReplyStartupKeyboard.add(KeyboardButton(cmd.buy_course_cmd))
