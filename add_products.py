from database import SessionLocal
from models import Product

def add_sample_products():
    db = SessionLocal()
    
    sample_products = [
        {"name": "Телевизор Sony", "price": 30000.99, "warranty_months": 24, "in_stock": 5},
        {"name": "Ноутбук HP", "price": 25000.99, "warranty_months": 12, "in_stock": 7},
        {"name": "Кофемашина DeLonghi", "price": 15000.99, "warranty_months": 18, "in_stock": 3}
    ]
    
    for item in sample_products:
        product = Product(**item)
        db.add(product)
    
    db.commit()
    print(f"Добавлено {len(sample_products)} товаров")

if __name__ == "__main__":
    add_sample_products()