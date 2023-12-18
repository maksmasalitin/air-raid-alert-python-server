import os
from dotenv import load_dotenv

load_dotenv()  # This loads the environment variables from .env

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default-secret-key')
    TELEGRAM_API_ID = os.getenv('TELEGRAM_API_ID')
    TELEGRAM_API_HASH = os.getenv('TELEGRAM_API_HASH')
    AUTH_KEYS = os.getenv('AUTH_KEYS', '').split(',')
