from aiogram import types

ADMIN_MENU_KB = types.InlineKeyboardMarkup()
ADMIN_MENU_KB.add(types.InlineKeyboardButton(text='🔍Найти пользователя', callback_data='searchUser'))
ADMIN_MENU_KB.add(types.InlineKeyboardButton(text='♻️Перезапуск бота', callback_data='restart'))