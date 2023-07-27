from flask import Blueprint, request, jsonify
from init import db
from models.stock import Stock, StockSchema

inventory_bp = Blueprint('inventory', __name__, url_prefix='/inventory')
stock_schema = StockSchema()
stocks_schema = StockSchema(many=True)

# Endpoint to create a new inventory item
@inventory_bp.route('/create', methods=['POST'])
def create_inventory_item():
    data = request.get_json()
    product_name = data.get('product_name')
    quantity = data.get('quantity')
    unit_price = data.get('unit_price')

    if not product_name or not quantity or not unit_price:
        return jsonify({'message': 'Missing required fields'}), 400

    new_item = Stock(product_name=product_name, quantity=quantity, unit_price=unit_price)
    db.session.add(new_item)
    db.session.commit()

    serialized_item = stock_schema.dump(new_item)
    return jsonify({'message': 'Inventory item created successfully', 'inventory_item': serialized_item}), 201