from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DateTime, Table, CheckConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base
product_accessory = Table(
    'product_accessory', Base.metadata,
    Column('product_id', Integer, ForeignKey('products.id', ondelete="CASCADE")),
    Column('accessory_id', Integer, ForeignKey('products.id', ondelete="CASCADE"))
)

class Product(Base):
    __tablename__ = 'products'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    price = Column(Float, CheckConstraint('price > 0'), nullable=False)
    warranty_months = Column(Integer, CheckConstraint('warranty_months >= 0'))
    in_stock = Column(Integer, CheckConstraint('in_stock >= 0'), default=0)
    is_active = Column(Boolean, default=True)
    
    accessories = relationship(
        "Product",
        secondary=product_accessory,
        primaryjoin=id == product_accessory.c.product_id,
        secondaryjoin=id == product_accessory.c.accessory_id,
        backref="compatible_with"
    )
    orders = relationship("OrderItem", back_populates="product")
    service_requests = relationship("ServiceRequest", back_populates="product")

class Customer(Base):
    __tablename__ = 'customers'
    
    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(Integer, unique=True, nullable=False)
    name = Column(String(100))
    credit_score = Column(Integer, CheckConstraint('credit_score BETWEEN 0 AND 1000'))
    phone = Column(String(20))
    
    orders = relationship("Order", back_populates="customer")
    service_requests = relationship("ServiceRequest", back_populates="customer")

class Order(Base):
    __tablename__ = 'orders'
    
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey('customers.id', ondelete="CASCADE"))
    status = Column(String(20), default='created')
    delivery_type = Column(String(30))
    payment_method = Column(String(30))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    customer = relationship("Customer", back_populates="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete")

class OrderItem(Base):
    __tablename__ = 'order_items'
    
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey('orders.id', ondelete="CASCADE"))
    product_id = Column(Integer, ForeignKey('products.id'))
    quantity = Column(Integer, CheckConstraint('quantity > 0'))
    
    order = relationship("Order", back_populates="items")
    product = relationship("Product", back_populates="orders")

class ServiceRequest(Base):
    __tablename__ = 'service_requests'
    
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey('customers.id', ondelete="CASCADE"))
    product_id = Column(Integer, ForeignKey('products.id'))
    issue = Column(String(500), nullable=False)
    status = Column(String(20), default='opened')
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    customer = relationship("Customer", back_populates="service_requests")
    product = relationship("Product", back_populates="service_requests")