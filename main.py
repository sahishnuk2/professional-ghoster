import asyncio
from aiogram import Dispatcher, Bot
from bot.config import TELEGRAM_BOT_TOKEN
from bot.handlers import messages


async def main():
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(messages.router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())

