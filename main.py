import os
from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from bot.config import TELEGRAM_BOT_TOKEN
from bot.handlers import messages

# Webhook settings
WEBHOOK_PATH = "/webhook"
PORT = int(os.environ.get("PORT", 10000))

# Will be set after deployment (your Render URL)
WEBHOOK_URL = os.environ.get("WEBHOOK_URL", "")

bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher()
dp.include_router(messages.router)


async def on_startup(app):
    if WEBHOOK_URL:
        await bot.set_webhook(f"{WEBHOOK_URL}{WEBHOOK_PATH}")
        print(f"Webhook set to {WEBHOOK_URL}{WEBHOOK_PATH}")
    else:
        print("WARNING: WEBHOOK_URL not set!")


async def on_shutdown(app):
    await bot.session.close()


def main():
    app = web.Application()
    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)

    # Setup webhook handler
    webhook_handler = SimpleRequestHandler(dispatcher=dp, bot=bot)
    webhook_handler.register(app, path=WEBHOOK_PATH)
    setup_application(app, dp, bot=bot)

    # Run web server
    web.run_app(app, host="0.0.0.0", port=PORT)


if __name__ == "__main__":
    main()
