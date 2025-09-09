# settings.py

import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DEBUG = os.getenv('DEBUG', 'False') == 'True'
    TOKEN = os.getenv('DISCORD_TOKEN')
    PREFIX = os.getenv('COMMAND_PREFIX', '!')
    DATABASE_URL = os.getenv('DATABASE_URL')
    SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key_here')
    ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '').split(',')
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')