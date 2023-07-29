from flask import Blueprint, request, jsonify
from init import db
from models.customers import Customer, CustomerSchema

customer_bp = Blueprint('customer', __name__, url_prefix='/customers')
customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)

# Endpoint to create a new customer
@customer_bp.route('/create', methods=['POST'])
def create_customer():
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

    new_customer = Customer(customer_number=customer_number, customer_name=customer_name, email=email, address=address)
    db.session.add(new_customer)
    db.session.commit()

    serialized_customer = customer_schema.dump(new_customer)
    return jsonify({'message': 'Customer created successfully', 'customer': serialized_customer}), 201

@customer_bp.route('/delete/<int:customer_id>', methods=['DELETE'])
def delete_customer(customer_id):
    customer = Customer.query.get(customer_id)

    if not customer:
        return jsonify({'message': 'Customer not found'}), 404

    db.session.delete(customer)
    db.session.commit()

    return jsonify({'message': 'Customer deleted successfully'}), 200

@customer_bp.route('/<int:customer_id>', methods=['GET'])
def get_customer(customer_id):
    customer = Customer.query.get(customer_id)

    if not customer:
        return jsonify({'message': 'Customer not found'}), 404

    serialized_customer = customer_schema.dump(customer)
    return jsonify({'customer': serialized_customer}), 200

@customer_bp.route('/update/<int:customer_id>', methods=['PUT'])
def update_customer(customer_id):
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

# Endpoint to get all customers
@customer_bp.route('/all', methods=['GET'])
def get_all_customers():
    # Retrieve all customers from the database
    all_customers = Customer.query.all()

    # Serialize the list of customers
    serialized_customers = customers_schema.dump(all_customers)

    return jsonify({'customers': serialized_customers}), 200