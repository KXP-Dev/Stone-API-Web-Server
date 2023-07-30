from flask import Blueprint, request, jsonify
from init import db
from models.customers import Customer, CustomerSchema
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required

customer_bp = Blueprint('customer', __name__, url_prefix='/customers')
customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)

# Endpoint to create a new customer
@customer_bp.route('/create', methods=['POST'])
@jwt_required()
def create_customer():
    try:
        current_user = get_jwt_identity()
        if not current_user['is_admin']:
            return jsonify({'error': 'You are not authorized to access this endpoint'}), 403

        data = request.get_json()
        customer_number = data.get('customer_number')
        customer_name = data.get('customer_name')
        email = data.get('email')
        address = data.get('address')

        # Input validation (you can add more validation as needed)
        if not customer_number or not customer_name or not email or not address:
            return jsonify({'message': 'Missing required fields'}), 400

        # Check if the customer with the given customer_number already exists
        if Customer.query.filter_by(customer_number=customer_number).first():
            return jsonify({'message': 'Customer with the given customer number already exists'}), 409

        # Create a new customer and add it to the database
        new_customer = Customer(customer_number=customer_number, customer_name=customer_name, email=email, address=address)
        db.session.add(new_customer)
        db.session.commit()
        serialized_customer = customer_schema.dump(new_customer)
        return jsonify({'message': 'Customer created successfully', 'customer': serialized_customer}), 201

    except Exception as e:
        return jsonify({'error': 'Internal Server Error'}), 500

@customer_bp.route('/delete/<int:customer_id>', methods=['DELETE'])
@jwt_required()
def delete_customer(customer_id):
    try:
        current_user = get_jwt_identity()
        if not current_user['is_admin']:
            return jsonify({'error': 'You are not authorized to access this endpoint'}), 403

        # Find the customer by the given customer_id
        customer = Customer.query.get(customer_id)
        if not customer:
            return jsonify({'message': 'Customer not found'}), 404

        # Delete the customer from the database
        db.session.delete(customer)
        db.session.commit()
        return jsonify({'message': 'Customer deleted successfully'}), 200

    except Exception as e:
        return jsonify({'error': 'Internal Server Error'}), 500

@customer_bp.route('/<int:customer_id>', methods=['GET'])
@jwt_required()
def get_customer(customer_id):
    try:
        customer = Customer.query.get(customer_id)
        if not customer:
            return jsonify({'message': 'Customer not found'}), 404
        serialized_customer = customer_schema.dump(customer)
        return jsonify({'customer': serialized_customer}), 200
    except Exception as e:
        return jsonify({'error': 'Internal Server Error'}), 500

@customer_bp.route('/update/<int:customer_id>', methods=['PUT'])
@jwt_required()
def update_customer(customer_id):
    try:
        customer = Customer.query.get(customer_id)
        if not customer:
            return jsonify({'message': 'Customer not found'}), 404
        data = request.get_json()
        customer_name = data.get('customer_name', customer.customer_name)
        email = data.get('email', customer.email)
        address = data.get('address', customer.address)
        customer_number = data.get('customer_number', customer.customer_number)
        customer.customer_name = customer_name
        customer.email = email
        customer.address = address
        customer.customer_number = customer_number
        db.session.commit()
        serialized_customer = customer_schema.dump(customer)
        return jsonify({'message': 'Customer updated successfully', 'customer': serialized_customer}), 200
    except Exception as e:
        return jsonify({'error': 'Internal Server Error'}), 500

    serialized_customer = customer_schema.dump(customer)
    return jsonify({'message': 'Customer updated successfully', 'customer': serialized_customer}), 200

# Endpoint to get all customers
@customer_bp.route('/all', methods=['GET'])
@jwt_required()
def get_all_customers():
    try:
        # Retrieve all customers from the database
        all_customers = Customer.query.all()
        # Serialize the list of customers
        serialized_customers = customers_schema.dump(all_customers)
        return jsonify({'customers': serialized_customers}), 200
    except Exception as e:
        return jsonify({'error': 'Internal Server Error'}), 500