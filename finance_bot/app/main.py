import asyncio
import logging

from create_bot import bot, dp
from handlers import client


logging.basicConfig(level=logging.INFO)


async def on_startup(_):
    print("Бот вышел в онлайн")


async def main():
    dp.include_router(client.router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
