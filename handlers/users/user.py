from aiogram import types
import sqlite3

from aiogram.types import ParseMode

from keyboards.inline.BACK_TO_MENU_KB import BACK_TO_MENU_KB
from loader import dp


@dp.callback_query_handler(text='userProfile', state='*')
async def userProfile(call: types.CallbackQuery):
    conn = sqlite3.connect("dataBase.db")
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM bot_users WHERE tgId = {call.from_user.id}")
    response = cursor.fetchone()
    await call.message.edit_text(f"➖➖➖➖➖➖➖➖➖➖\n"
                                 f"👤<b>Пользователь:</b> <code>{response[0]}</code>\n"
                                 f"💵<b>Баланс в боте:</b> <code>{response[1]}</code>\n"
                                 f"➖➖➖➖➖➖➖➖➖➖", parse_mode=ParseMode.HTML)
    await call.message.edit_reply_markup(reply_markup=BACK_TO_MENU_KB)
    await call.answer()