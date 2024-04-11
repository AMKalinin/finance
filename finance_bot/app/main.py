import asyncio
import logging

from aiogram_dialog import setup_dialogs

from create_bot import bot, dp
from handlers import client


logging.basicConfig(level=logging.INFO)


async def main():
    dp.include_router(client.router)
    setup_dialogs(dp)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
