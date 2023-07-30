from flask import Blueprint, request, jsonify
from init import db
from models.orders import Order, OrderSchema
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required

order_bp = Blueprint('order', __name__, url_prefix='/orders')
order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)

# Endpoint to create a new order (Requires jwt and admin access)
@order_bp.route('/create', methods=['POST'])
@jwt_required()
def create_order():
    try:
        current_user = get_jwt_identity()

        # Check if the current user is an admin
        if not current_user.get('is_admin'):
            return jsonify({'error': 'You are not authorized to create orders'}), 403

        # Get data from the request JSON
        data = request.get_json()
        customer_id = data.get('customer_id')
        total_amount = data.get('total_amount')
        
        # Input validation (you can add more validation as needed)
        if not customer_id or not total_amount:
            return jsonify({'message': 'Missing required fields'}), 400

        # Create a new order instance and add it to the database
        new_order = Order(customer_id=customer_id, total_amount=total_amount)
        db.session.add(new_order)
        db.session.commit()

        # Serialize the new order and return the response
        serialized_order = order_schema.dump(new_order)
        return jsonify({'message': 'Order created successfully', 'order': serialized_order}), 201
    except Exception as e:
        return jsonify({'error': 'Internal Server Error'}), 500

@order_bp.route('/all', methods=['GET'])
@jwt_required()
def get_all_orders():
    try:
        # Retrieve all orders from the database
        orders = Order.query.all()
        
        # Serialize the list of orders and return the response
        serialized_orders = orders_schema.dump(orders)
        return jsonify({'orders': serialized_orders}), 200
    except Exception as e:
        return jsonify({'error': 'Internal Server Error'}), 500


@order_bp.route('/delete/<int:order_id>', methods=['DELETE'])
@jwt_required()
def delete_order(order_id):
    try:
        current_user = get_jwt_identity()

        # Check if the current user is an admin
        if not current_user.get('is_admin'):
            return jsonify({'error': 'You are not authorized to delete orders'}), 403

        # Retrieve the order by order_id from the database
        order = Order.query.get(order_id)

        # Check if the order_id is provided and if the order exists
        if not order_id:
            return jsonify({'message': 'Order ID not provided'}), 400

        if not order:
            return jsonify({'message': 'Order not found'}), 404

        # Delete the order from the database and commit the changes
        db.session.delete(order)
        db.session.commit()

        return jsonify({'message': 'Order deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': 'Internal Server Error'}), 500

@order_bp.route('/update/<int:order_id>', methods=['PUT'])
@jwt_required()
def update_order(order_id):
    try:
        # Retrieve the order by order_id from the database
        order = Order.query.get(order_id)

        # Check if the order exists
        if not order:
            return jsonify({'message': 'Order not found'}), 404

        # Get data from the request JSON
        data = request.get_json()
        total_amount = data.get('total_amount', order.total_amount)

        # Update the total amount of the order and commit the changes
        order.total_amount = total_amount
        db.session.commit()

        # Serialize the updated order and return the response
        serialized_order = order_schema.dump(order)
        return jsonify({'message': 'Order updated successfully', 'order': serialized_order}), 200
    except Exception as e:
        return jsonify({'error': 'Internal Server Error'}), 500
