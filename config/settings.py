import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
DATABASE_URL = os.getenv("DATABASE_URL")
REDIS_URL = os.getenv("REDIS_URL")
SECRET_KEY = os.getenv("SECRET_KEY")
DEBUG = os.getenv("DEBUG", "False") == "True"

if not all([TELEGRAM_BOT_TOKEN, DATABASE_URL, REDIS_URL, SECRET_KEY]):
    raise ValueError("Missing environment variables. Please set TELEGRAM_BOT_TOKEN, DATABASE_URL, REDIS_URL, and SECRET_KEY.")

```