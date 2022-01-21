from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import commands as cmd

buttons = [cmd.buy_course_cmd]
startup_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
startup_keyboard.add(KeyboardButton(cmd.buy_course_cmd))
