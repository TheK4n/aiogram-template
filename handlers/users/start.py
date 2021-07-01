from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from loader import bot, dp, db


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    msg_from_usr = message.from_user

    bot_username = (await bot.me).username
    bot_link = f"https://t.me/{bot_username}?start={msg_from_usr.id}"
    referral = message.get_args()

    if db.get_user_data(msg_from_usr.id) is None:
        await message.answer(f"{message.from_user.full_name}, вы впервые запустили бота!\n"
                             f"Выша реферальная ссылка: {bot_link}")
        db.add_new_user(msg_from_usr.id, msg_from_usr.username, msg_from_usr.first_name,
                        msg_from_usr.last_name, referral=referral)
    else:
        await message.answer(f"Привет, {message.from_user.full_name}!\n"
                             f"Выша реферальная ссылка: {bot_link}")
