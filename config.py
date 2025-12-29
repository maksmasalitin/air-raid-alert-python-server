import os
from dotenv import load_dotenv

load_dotenv()  # This loads the environment variables from .env

class Config:
    TELEGRAM_API_ID = os.getenv('TELEGRAM_API_ID')
    TELEGRAM_API_HASH = os.getenv('TELEGRAM_API_HASH')
    TELEGRAM_SESSION_FILE_PATH = 'telegram-session'
    AUTH_KEYS = os.getenv('AUTH_KEYS', '').split(',')
