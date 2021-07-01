from aiogram import types
from aiogram.dispatcher.filters.builtin import Command

from loader import dp, db


@dp.message_handler(Command('balance'))
async def bot_balance(message: types.Message):
    await message.answer(f'Ваш баланс: {db.get_user_balance(message.chat.id)} руб.')
