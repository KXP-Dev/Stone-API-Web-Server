from init import db, ma
from sqlalchemy import Column, Integer, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship

class Customer(db.Model):
    __tablename__ = 'customers'
    
    customer_id = db.Column(db.Integer, primary_key=True)
    customer_number = db.Column(db.String(20), unique=True, nullable=False)
    customer_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    address = db.Column(db.String(200), nullable=False)
    
    # Define the back-reference for the 'orders' relationship
    orders = relationship('Order', back_populates='customer')

class CustomerSchema(ma.Schema):
    class Meta:
        fields = ('customer_id', 'customer_number', 'customer_name', 'email', 'address')