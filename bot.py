import telebot
from config import TELEGRAM_TOKEN, ADMIN_CHAT_ID
from database import Base, engine
from commands import setup_commands


Base.metadata.create_all(bind=engine)


bot = telebot.TeleBot(TELEGRAM_TOKEN)


setup_commands(bot)


if __name__ == '__main__':
    print("Бот запущен...")
    bot.infinity_polling()