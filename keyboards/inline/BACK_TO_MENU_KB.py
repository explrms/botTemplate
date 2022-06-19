from aiogram import types

BACK_TO_MENU_KB = types.InlineKeyboardMarkup()
BACK_TO_MENU_KB.add(types.InlineKeyboardButton(text='🔙Назад в меню', callback_data='mainMenu'))