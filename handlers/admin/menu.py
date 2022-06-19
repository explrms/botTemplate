import sqlite3

from aiogram import types
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import ParseMode

from data.config import ADMINS
from keyboards.inline.ADMIN_MENU_KB import ADMIN_MENU_KB
from loader import dp


class adminState(StatesGroup):
    userSearch = State()
    finish = State()


@dp.message_handler(state='*', commands=['admin'])
async def adminMenu(message: types.Message):
    if message.from_user.id in ADMINS:
        await message.answer("⚙️Вы находитесь в панели управления", reply_markup=ADMIN_MENU_KB)
    else:
        await message.answer(f"🛑У вас нет доступа в этот раздел. Если вы администратор проекта — предоставьте ваш ig "
                             f"<code>{message.from_user.id}</code> другому авторизованному администратору для "
                             f"добавления в white-list.", parse_mode=ParseMode.HTML)


@dp.callback_query_handler(text='searchUser', state='*')
async def searchUser(call: types.CallbackQuery):
    await call.message.edit_text("Введите id пользователя в Telegram:")
    await adminState.userSearch.set()


@dp.message_handler(state=adminState.userSearch)
async def userSearchInput(message: types.Message):
    if message.text.isdigit():
        conn = sqlite3.connect("dataBase.db")
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM bot_users WHERE tgId = {message.text}")
        response = cursor.fetchone()
        if response is None:
            await message.answer("❌Пользователь не найден в базе.")
        else:
            await message.answer(f"<b>👤Пользователь(<code>{response[0]}</code>)</b>\n"
                                 f"<b>💵Баланс в боте:</b> {response[1]}", parse_mode=ParseMode.HTML)
            await adminState.finish.set()
    else:
        await message.answer("Вы должны ввести id пользователя.\n"
                             "Подсказка: узнать можно командой /getid")


@dp.callback_query_handler(state='*', text='restart')
async def restartBotText(call: types.CallbackQuery):
    if call.from_user.id in ADMINS:
        import os
        import sys
        await call.message.answer("⏳Бот будет перезапущен. . .")
        await call.answer()
        os.system("sh restart.sh")
        sys.exit()
