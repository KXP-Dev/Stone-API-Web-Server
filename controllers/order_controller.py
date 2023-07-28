from flask import Blueprint, request, jsonify
from init import db
from models.orders import Order, OrderSchema

order_bp = Blueprint('order', __name__, url_prefix='/orders')
order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)

@order_bp.route('/create', methods=['POST'])
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