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