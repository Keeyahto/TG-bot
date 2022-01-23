from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def create_dynamic_inline_keyboard(texts: list, row_width=1, callback_data_prefix=''):
    keyboard = InlineKeyboardMarkup(row_width=row_width)
    for text in texts:
        keyboard.insert(InlineKeyboardButton(text=text, callback_data=callback_data_prefix + str(text)))
    return keyboard

__months = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май']
InlineMonthKeyboard = create_dynamic_inline_keyboard(__months, row_width=3)