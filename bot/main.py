import asyncio
import logging

from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, Application, Dispatcher, CallbackContext

from bot.telegram_bot import start, register, send, balance, history, error_callback
from config import settings
from database import db_setup

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

async def main():
    await db_setup.database_setup()
    application = ApplicationBuilder().token(settings.TELEGRAM_BOT_TOKEN).build()
    dp:Dispatcher = application.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("register", register))
    dp.add_handler(CommandHandler("send", send))
    dp.add_handler(CommandHandler("balance", balance))
    dp.add_handler(CommandHandler("history", history))
    dp.add_error_handler(error_callback)

    await application.run_polling()

if __name__ == "__main__":
    asyncio.run(main())

```