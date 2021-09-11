from aiogram import executor

from loader import dp, db
import middlewares, filters, handlers
from utils.notify_admins import on_startup_notify, on_shutdown_notify
from utils.set_bot_commands import set_default_commands


async def on_startup(dispatcher):
    # Устанавливаем дефолтные команды
    await set_default_commands(dispatcher)

    # Уведомляет о запуске
    await on_startup_notify(dispatcher)


async def on_shutdown(dp):

    # Уведомляет об выключении
    await on_shutdown_notify(dp)

    dp.stop_polling()

    # закрывает бд
    db.close()


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)
