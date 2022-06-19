from aiogram import types
import sqlite3

from aiogram.types import ParseMode

from loader import dp
from keyboards.inline.MAIN_MENU_KB import MAIN_MENU_KB


async def writeUserDataToDb(userid):
    conn = sqlite3.connect("dataBase.db")
    cursor = conn.cursor()
    count = cursor.execute(f"SELECT COUNT(*) FROM bot_users WHERE tgId = {userid}").fetchone()[0]
    if count == 0:
        cursor.execute(f"INSERT INTO bot_users (tgId, balance) VALUES ({userid}, 0)")
        conn.commit()
        conn.close()


@dp.message_handler(state='*', commands=['start'])
async def mainMenuMessage(message: types.Message):
    await message.answer(f"👋Привет, {message.from_user.full_name}!\n\n"
                         f"Я – бот для создания платежей.\n"
                         f"⬇️Нажмите на кнопку, чтобы пополнить баланс.", reply_markup=MAIN_MENU_KB)
    await writeUserDataToDb(message.from_user.id)


@dp.message_handler(state='*', commands=['getid'])
async def getId(message: types.Message):
    await message.answer(f"Ваш id: <code>{message.from_user.id}</code>", parse_mode=ParseMode.HTML)


@dp.callback_query_handler(state='*', text='mainMenu')
async def mainMenuCallback(call: types.CallbackQuery):
    await call.message.edit_text(f"👋Привет, {call.from_user.full_name}!\n\n"
                                 f"Я – бот для создания платежей.\n"
                                 f"⬇️Нажмите на кнопку, чтобы пополнить баланс.")
    await call.message.edit_reply_markup(reply_markup=MAIN_MENU_KB)
    await call.answer()


@dp.message_handler(commands=['help'], state='*')
async def help(message: types.Message):
    await message.answer("Доступные команды:\n"
                         "/start — запуск бота и главное меню\n"
                         "/help — список всех команд\n"
                         "/getid — узнать id Telegram")
