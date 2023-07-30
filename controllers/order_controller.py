from flask import Blueprint, request, jsonify
from init import db
from models.orders import Order, OrderSchema
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required

order_bp = Blueprint('order', __name__, url_prefix='/orders')
order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)

@order_bp.route('/create', methods=['POST'])
@jwt_required()
def create_order():
    data = request.get_json()
    customer_id = data.get('customer_id')
    total_amount = data.get('total_amount')
    if not customer_id or not total_amount:
        return jsonify({'message': 'Missing required fields'}), 400
    new_order = Order(customer_id=customer_id, total_amount=total_amount)
    db.session.add(new_order)
    db.session.commit()

    serialized_order = order_schema.dump(new_order)
    return jsonify({'message': 'Order created successfully', 'order': serialized_order}), 201

@order_bp.route('/all', methods=['GET'])
def get_all_orders():
    orders = Order.query.all()
    serialized_orders = orders_schema.dump(orders)
    return jsonify({'orders': serialized_orders}), 200

@order_bp.route('/delete/<int:order_id>', methods=['DELETE'])
@jwt_required()
def delete_order(order_id):
    order = Order.query.get(order_id)

    if not order_id:
        return jsonify({'message': 'Order ID not provided'}), 400

    if not order:
        return jsonify({'message': 'Order not found'}), 404

    db.session.delete(order)
    db.session.commit()

    return jsonify({'message': 'Order deleted successfully'}), 200

@order_bp.route('/update/<int:order_id>', methods=['PUT'])
@jwt_required()
def update_order(order_id):
    order = Order.query.get(order_id)

    if not order:
        return jsonify({'message': 'Order not found'}), 404

    data = request.get_json()
    total_amount = data.get('total_amount', order.total_amount)

    order.total_amount = total_amount

    db.session.commit()

    serialized_order = order_schema.dump(order)
    return jsonify({'message': 'Order updated successfully', 'order': serialized_order}), 200