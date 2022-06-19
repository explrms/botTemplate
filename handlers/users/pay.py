import random
import sqlite3
from pprint import pprint

from aiogram import types
from aiogram.dispatcher.filters import Regexp
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import ParseMode
from pyqiwip2p import AioQiwiP2P

from data.config import QIWI_PRIV_KEY
from keyboards.inline.BACK_TO_MENU_KB import BACK_TO_MENU_KB
from loader import dp
from utils.notify_admins import admin_notify

p2p = AioQiwiP2P(auth_key=QIWI_PRIV_KEY)


class payState(StatesGroup):
    amount = State()
    finish = State()


@dp.callback_query_handler(state='*', text='pay')
async def pay(call: types.CallbackQuery):
    await call.message.edit_text("✏️Введите сумму пополнения:")
    await call.message.edit_reply_markup(reply_markup=BACK_TO_MENU_KB)
    await payState.amount.set()
    await call.answer()


@dp.message_handler(state=payState.amount)
async def amountInput(message: types.Message):
    if message.text.isdigit():
        msg = await message.answer("⌛Создаём счет. . .")
        new_bill = await p2p.bill(bill_id=random.randint(10000, 99999), amount=int(message.text), lifetime=5)
        kb = types.InlineKeyboardMarkup()
        kb.add(types.InlineKeyboardButton(text='💲Перейти к оплате', url=f'{new_bill.pay_url}'))
        kb.add(types.InlineKeyboardButton(text='✅Проверить платёж', callback_data=f'checkPay:{new_bill.bill_id}'),
               types.InlineKeyboardButton(text='❌Отменить платёж', callback_data=f'cancelPay:{new_bill.bill_id}'))
        await dp.bot.edit_message_text(chat_id=msg["chat"]["id"],
                                       message_id=msg['message_id'],
                                       text=f"<b>Выставлен счёт №</b><code>{new_bill.bill_id}</code>\n"
                                       f"<b>Сумма:</b> <code>{new_bill.amount}</code>",
                                       parse_mode=ParseMode.HTML)
        await dp.bot.edit_message_reply_markup(chat_id=msg["chat"]["id"],
                                               message_id=msg['message_id'],
                                               reply_markup=kb)
        await payState.finish.set()
    else:
        await message.answer("❌Вы должны ввести целое число!", reply_markup=BACK_TO_MENU_KB)


@dp.callback_query_handler(Regexp('checkPay'), state='*')
async def checkPay(call: types.CallbackQuery):
    bill_id = call.data.replace('checkPay:', '')
    bill = (await p2p.check(bill_id=bill_id))
    if bill.status == 'PAID':
        try:
            conn = sqlite3.connect("dataBase.db")
            cursor = conn.cursor()
            cursor.execute(f"UPDATE bot_users SET balance = balance + {bill.amount}")
            conn.commit()
            conn.close()
        except Exception as ex:
            await admin_notify(dp, text=f"❗❗❗Пользователь {call.from_user.username} пополнил баланс, но данные не записались в базу.\n"
                               f"id платежа: {bill.bill_id}\n"
                               f"сумма: {bill.amount}")
        await call.message.edit_text(f"✅Счёт №<code>{bill_id}</code> успешно оплачен.", parse_mode=ParseMode.HTML)
        await call.message.edit_reply_markup(reply_markup=BACK_TO_MENU_KB)
        await call.answer()
    else:
        await call.answer("❌Платёж не найден. Попробуйте через несколько секунд.", show_alert=True)


@dp.callback_query_handler(Regexp('cancelPay'), state='*')
async def cancelPay(call: types.CallbackQuery):
    bill_id = call.data.replace('cancelPay:', '')
    await p2p.reject(bill_id=bill_id)
    await call.message.edit_text("✅Платёж отменён.")
    await call.message.edit_reply_markup(reply_markup=BACK_TO_MENU_KB)
    await call.answer()