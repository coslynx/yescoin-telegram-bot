import logging
from telegram import Update, ParseMode
from telegram.error import TelegramError
from loguru import logger

def setup_logger():
    logger.remove()
    logger.add("error.log", level="ERROR", rotation="10 MB", compression="zip")

setup_logger()


async def handle_error(update: Update, context: Update.ContextTypes, error: Exception):
    logger.exception(f"Error occurred: {error}")
    try:
        if update and update.effective_message:
            await update.effective_message.reply_text(
                "An error occurred. Please try again later.", parse_mode=ParseMode.HTML
            )
        else:
            logger.error(f"Update or message not found for error: {error}")
    except TelegramError as e:
        logger.error(f"Telegram error while sending error message: {e}")

```