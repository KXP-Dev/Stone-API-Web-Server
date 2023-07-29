from init import db, ma
from sqlalchemy import Column, Integer, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship

class Order(db.Model):
    __tablename__ = 'orders'
    order_id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('customers.customer_id'), nullable=False)
    total_amount = Column(Float, nullable=False)

    # Define the relationship with Customer and Stock models
    customer = relationship('Customer', back_populates='orders')

class OrderSchema(ma.Schema):
    class Meta:
        fields = ('order_id', 'customer_id', 'total_amount')