from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
import commands as cmd

buttons = [cmd.upload_course_cmd]
#startup_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
#startup_keyboard.add(KeyboardButton(cmd.upload_course_cmd))
dont_upload = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(KeyboardButton('/stop'))