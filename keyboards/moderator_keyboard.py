from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
import commands as cmd

Dont_upload = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(KeyboardButton('/stop'))
Moderator_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
Moderator_keyboard.add(KeyboardButton(cmd.upload_course_cmd))
