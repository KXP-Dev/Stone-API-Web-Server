from init import db, ma
from sqlalchemy import Column, Integer, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship

class Stock(db.Model):
    __tablename__ = 'stock'
    
    product_id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, default=0, nullable=False)
    unit_price = db.Column(db.Float, nullable=False)

class StockSchema(ma.Schema):
    class Meta:
        fields = ('product_id', 'product_name', 'quantity', 'unit_price')