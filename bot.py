import telebot
from config import TELEGRAM_TOKEN, ADMIN_CHAT_ID
from database import Base, engine
from commands import setup_commands

# Создаем таблицы в БД
Base.metadata.create_all(bind=engine)

# Инициализация бота
bot = telebot.TeleBot(TELEGRAM_TOKEN)

# Настройка команд
setup_commands(bot)

# Запуск бота
if __name__ == '__main__':
    print("Бот запущен...")
    bot.infinity_polling()