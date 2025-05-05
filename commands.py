from telebot import types
from models import Product, Customer, Order, ServiceRequest
from database import get_db
from config import ADMIN_CHAT_ID

def setup_commands(bot):
    @bot.message_handler(commands=['start'])
    def start(message):
        db = next(get_db())
        customer = db.query(Customer).filter(Customer.telegram_id == message.from_user.id).first()
        
        if not customer:
            customer = Customer(
                telegram_id=message.from_user.id,
                name=message.from_user.first_name
            )
            db.add(customer)
            db.commit()
        
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add('📦 Товары', '🛒 Мои заказы')
        markup.add('🔧 Сервис', '💳 Кредитные предложения')
        
        bot.send_message(
            message.chat.id,
            f"Добро пожаловать, {message.from_user.first_name}!\nВыберите действие:",
            reply_markup=markup
        )

    @bot.message_handler(func=lambda message: message.text == '📦 Товары')
    def show_products(message):
        db = next(get_db())
        products = db.query(Product).filter(Product.is_active == True).limit(10).all()
        
        if not products:
            bot.send_message(message.chat.id, "Товары не найдены.")
            return
        
        for product in products:
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton(
                "Добавить в корзину", 
                callback_data=f"add_to_cart_{product.id}"))
            
            bot.send_message(
                message.chat.id,
                f"{product.name}\nЦена: {product.price} руб.\nНа складе: {product.in_stock} шт.",
                reply_markup=markup
            )

    @bot.callback_query_handler(func=lambda call: call.data.startswith('add_to_cart_'))
    def add_to_cart(call):
        product_id = int(call.data.split('_')[-1])
        db = next(get_db())
        
        product = db.query(Product).get(product_id)
        bot.answer_callback_query(call.id, f"{product.name} добавлен в корзину!")

    @bot.message_handler(commands=['add_product'])
    def add_product_command(message):
        if message.from_user.id != ADMIN_CHAT_ID:
            bot.send_message(message.chat.id, "У вас нет прав на эту операцию")
            return
        
        msg = bot.send_message(message.chat.id, "Введите название товара:")
        bot.register_next_step_handler(msg, process_product_name_step)

    def process_product_name_step(message):
        try:
            product_data = {'name': message.text}
            msg = bot.send_message(message.chat.id, "Введите цену товара:")
            bot.register_next_step_handler(msg, process_product_price_step, product_data)
        except Exception as e:
            bot.reply_to(message, f"Ошибка: {e}")

    def process_product_price_step(message, product_data):
        try:
            product_data['price'] = float(message.text)
            msg = bot.send_message(message.chat.id, "Введите гарантийный срок (в месяцах):")
            bot.register_next_step_handler(msg, process_product_warranty_step, product_data)
        except ValueError:
            msg = bot.send_message(message.chat.id, "Цена должна быть числом. Попробуйте еще раз:")
            bot.register_next_step_handler(msg, process_product_price_step, product_data)
        except Exception as e:
            bot.reply_to(message, f"Ошибка: {e}")

    def process_product_warranty_step(message, product_data):
        try:
            product_data['warranty_months'] = int(message.text)
            msg = bot.send_message(message.chat.id, "Введите количество на складе:")
            bot.register_next_step_handler(msg, process_product_stock_step, product_data)
        except ValueError:
            msg = bot.send_message(message.chat.id, "Срок должен быть целым числом. Попробуйте еще раз:")
            bot.register_next_step_handler(msg, process_product_warranty_step, product_data)
        except Exception as e:
            bot.reply_to(message, f"Ошибка: {e}")

    def process_product_stock_step(message, product_data):
        try:
            product_data['in_stock'] = int(message.text)
            
            db = next(get_db())
            product = Product(
                name=product_data['name'],
                price=product_data['price'],
                warranty_months=product_data['warranty_months'],
                in_stock=product_data['in_stock']
            )
            db.add(product)
            db.commit()
            
            bot.send_message(message.chat.id, "Товар успешно добавлен!")
        except ValueError:
            msg = bot.send_message(message.chat.id, "Количество должно быть целым числом. Попробуйте еще раз:")
            bot.register_next_step_handler(msg, process_product_stock_step, product_data)
        except Exception as e:
            bot.reply_to(message, f"Ошибка: {e}")