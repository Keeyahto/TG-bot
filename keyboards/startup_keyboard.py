from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
import commands as cmd

startup_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
startup_keyboard.add(KeyboardButton(cmd.buy_course_cmd))
