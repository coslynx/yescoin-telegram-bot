import logging
from telegram import Update, ForceReply
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

from services import user_service, transaction_service, coin_service
from utils import error_handling, input_validation

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = await user_service.get_user(update.effective_user.id)
    if user:
        await update.message.reply_text(f"Welcome back, {user.username}!")
    else:
        await update.message.reply_text(
            "Welcome to YesCoin! Use /register to get started."
        )

async def register(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await input_validation.validate_registration(update.message.text)
        await user_service.register_user(update.effective_user.id, update.message.text)
        await update.message.reply_text("Registration successful!")
    except Exception as e:
        await error_handling.handle_error(update, context, e)


async def send(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await input_validation.validate_transaction(update.message.text)
        await transaction_service.process_transaction(update.effective_user.id, update.message.text)
        await update.message.reply_text("Transaction successful!")

    except Exception as e:
        await error_handling.handle_error(update, context, e)


async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        balance = await user_service.get_balance(update.effective_user.id)
        await update.message.reply_text(f"Your balance: {balance} YesCoins")
    except Exception as e:
        await error_handling.handle_error(update, context, e)


async def history(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        history = await transaction_service.get_transaction_history(update.effective_user.id)
        await update.message.reply_text(history)
    except Exception as e:
        await error_handling.handle_error(update, context, e)



async def error_callback(update: object, context: ContextTypes.DEFAULT_TYPE):
    await error_handling.handle_error(update, context, context.error)


if __name__ == '__main__':
    from config import settings
    application = ApplicationBuilder().token(settings.TELEGRAM_BOT_TOKEN).build()

    start_handler = CommandHandler('start', start)
    register_handler = CommandHandler('register', register)
    send_handler = CommandHandler('send', send)
    balance_handler = CommandHandler('balance', balance)
    history_handler = CommandHandler('history', history)

    application.add_handler(start_handler)
    application.add_handler(register_handler)
    application.add_handler(send_handler)
    application.add_handler(balance_handler)
    application.add_handler(history_handler)
    application.add_error_handler(error_callback)

    application.run_polling()
```