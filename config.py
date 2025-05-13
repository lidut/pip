from dotenv import load_dotenv
import os

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
DATABASE_URL = os.getenv('DATABASE_URL')
ADMIN_CHAT_ID = 890188684