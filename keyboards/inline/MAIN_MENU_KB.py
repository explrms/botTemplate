from aiogram import types

MAIN_MENU_KB = types.InlineKeyboardMarkup()
MAIN_MENU_KB.add(types.InlineKeyboardButton(text='💰Пополнить баланс', callback_data='pay'))
MAIN_MENU_KB.add(types.InlineKeyboardButton(text='👤Личный кабинет', callback_data='userProfile'))
