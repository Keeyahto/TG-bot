from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import commands as cmd

Startup_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
Startup_keyboard.add(KeyboardButton(cmd.buy_course_cmd))
