import logging
from loguru import logger

def setup_logger():
    logger.remove()
    logger.add("logs/yescoin_bot.log", level="DEBUG", rotation="10 MB", compression="zip",
               format="{time} | {level} | {message}")

setup_logger()

def log_info(message):
    logger.info(message)

def log_debug(message):
    logger.debug(message)

def log_warning(message):
    logger.warning(message)

def log_error(message, exception=None):
    if exception:
        logger.exception(f"{message}: {exception}")
    else:
        logger.error(message)

def log_critical(message, exception=None):
    if exception:
        logger.exception(f"{message}: {exception}")
    else:
        logger.critical(message)

```