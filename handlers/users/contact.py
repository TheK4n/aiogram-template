from aiogram import types

from loader import dp, db


@dp.message_handler(content_types='contact')
async def bot_start(message: types.Message):
    await message.answer('Вы отправили нам свой номер!')
    db.update_user_data(message.from_user.id, 'PhoneNumber', message.contact.phone_number)
