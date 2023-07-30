from flask import Blueprint, request, jsonify
from init import db
from models.stock import Stock, StockSchema
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required

inventory_bp = Blueprint('inventory', __name__, url_prefix='/inventory')
stock_schema = StockSchema()
stocks_schema = StockSchema(many=True)

# Endpoint to create a new inventory item
@inventory_bp.route('/create', methods=['POST'])
@jwt_required()
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

@inventory_bp.route('/delete', methods=['DELETE'])
@jwt_required()
def delete_inventory_item():
    data = request.get_json()
    product_id = data.get('product_id')

    if not product_id:
        return jsonify({'message': 'Missing required field: product_id'}), 400

    item_to_delete = Stock.query.get(product_id)
    if not item_to_delete:
        return jsonify({'message': 'Inventory item not found'}), 404

    db.session.delete(item_to_delete)
    db.session.commit()

    return jsonify({'message': 'Inventory item deleted successfully'}), 200

@inventory_bp.route('/update', methods=['PUT'])
@jwt_required()
def update_inventory_item():
    data = request.get_json()
    product_id = data.get('product_id')
    product_name = data.get('product_name')
    quantity = data.get('quantity')
    unit_price = data.get('unit_price')

    if not product_id:
        return jsonify({'message': 'Missing required field: product_id'}), 400

    item_to_update = Stock.query.get(product_id)
    if not item_to_update:
        return jsonify({'message': 'Inventory item not found'}), 404

    # Update the item's fields if provided in the request
    if product_name:
        item_to_update.product_name = product_name
    if quantity:
        item_to_update.quantity = quantity
    if unit_price:
        item_to_update.unit_price = unit_price

    db.session.commit()

    serialized_item = stock_schema.dump(item_to_update)
    return jsonify({'message': 'Inventory item updated successfully', 'inventory_item': serialized_item}), 200

@inventory_bp.route('/all', methods=['GET'])
def get_all_inventory_items():
    all_items = Stock.query.all()
    serialized_items = stocks_schema.dump(all_items)
    return jsonify({'inventory_items': serialized_items}), 200