from flask import Blueprint, request
from init import db, bcrypt
from models.employee import Employee, employee_schema, employees_schema
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes
from datetime import timedelta
from flask import jsonify

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['POST'])
def auth_register():
    try:
        body_data = request.get_json()
        
        # Validate required fields
        required_fields = ['employee_name', 'employee_email', 'password']
        for field in required_fields:
            if field not in body_data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Check if email address is already in use
        existing_employee = Employee.query.filter_by(employee_email=body_data['employee_email']).first()
        if existing_employee:
            return jsonify({'error': 'Email address already in use'}), 409

        # Create a new Employee model instance from the user info.
        employee = Employee()
        employee.employee_name = body_data['employee_name']
        employee.employee_email = body_data['employee_email']
        employee.password = bcrypt.generate_password_hash(body_data['password']).decode('utf-8')

        # Add the employee to the session.
        db.session.add(employee)
        # Commit to add the employee to the database.
        db.session.commit()

        # Respond to the client.
        return employee_schema.dump(employee), 201
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return jsonify({'error': 'Email address already in use'}), 409
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            column_name = err.orig.diag.column_name
            return jsonify({'error': f'The {column_name} is required'}), 400
        return jsonify({'error': 'Internal Server Error'}), 500
        
@auth_bp.route('/login', methods=['POST'])
def auth_login():
    try:
        body_data = request.get_json()

        # Validate required fields
        required_fields = ['employee_email', 'password']
        for field in required_fields:
            if field not in body_data:
                return jsonify({'error': f'Missing required field: {field}'}), 400

        # Find the user by email address
        employee = Employee.query.filter_by(employee_email=body_data['employee_email']).first()

        # If employee exists and password is correct
        if employee and bcrypt.check_password_hash(employee.password, body_data['password']):
            # Create a dictionary to hold user information for the JWT token
            identity = {
                'employee_id': employee.employee_id,
                'is_admin': employee.is_admin
            }
            # Generate the JWT token with the identity and set the expiration time
            token = create_access_token(identity=identity, expires_delta=timedelta(days=1))
            return jsonify({'employee_email': employee.employee_email, 'token': token}), 200
        else:
            return jsonify({'error': 'Invalid email or password'}), 401
    except Exception as e:
        return jsonify({'error': 'Internal Server Error'}), 500
    
@auth_bp.route('/check-admin', methods=['POST'])
@jwt_required()
def check_admin():
    current_user = get_jwt_identity()

    # Print the current_user dictionary to see its contents
    print(current_user)

    user_id_key = 'employee_id'

    if user_id_key in current_user:
        current_user_id = current_user.get('employee_id')
        # Query the database to fetch the employee by the current_user_id
        employee = Employee.query.get(current_user_id)

        if employee.is_admin:
            return jsonify({'message': 'User is an admin'}), 200
        else:
            return jsonify({'message': 'User is not an admin'}), 403
    else:
        return jsonify({'message': 'User ID not found in JWT token'}), 400
    
@auth_bp.route('/delete/<int:employee_id>', methods=['DELETE'])
@jwt_required()
def delete_employee(employee_id):
    try:
        current_user = get_jwt_identity()
        # Query the database to fetch the employee by the given employee_id
        employee = Employee.query.get(employee_id)

        if not employee:
            return jsonify({'error': 'Employee not found'}), 404

        if employee.employee_id == current_user['employee_id']:
            return jsonify({'error': 'You cannot delete your own account'}), 403

        if not current_user['is_admin']:
            return jsonify({'error': 'You are not authorized to delete employees'}), 403

        # Delete the employee from the database
        db.session.delete(employee)
        db.session.commit()

        return jsonify({'message': 'Employee deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': 'Internal Server Error'}), 500
    
@auth_bp.route('/update/<int:employee_id>', methods=['PUT'])
@jwt_required()
def update_employee(employee_id):
    try:
        current_user = get_jwt_identity()
        # Query the database to fetch the employee by the given employee_id
        employee = Employee.query.get(employee_id)

        if not employee:
            return jsonify({'error': 'Employee not found'}), 404

        if employee.employee_id == current_user['employee_id']:
            return jsonify({'error': 'You cannot update your own account'}), 403

        if not current_user['is_admin']:
            return jsonify({'error': 'You are not authorized to update employee information'}), 403

        data = request.get_json()
        employee_name = data.get('employee_name', employee.employee_name)
        employee_email = data.get('employee_email', employee.employee_email)
        is_admin = data.get('is_admin', employee.is_admin)

        # Update the employee information in the database
        employee.employee_name = employee_name
        employee.employee_email = employee_email
        employee.is_admin = is_admin

        db.session.commit()

        return jsonify({'message': 'Employee information updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': 'Internal Server Error'}), 500
    
@auth_bp.route('/employees', methods=['GET'])
@jwt_required()
def get_all_employees():
    try:
        current_user = get_jwt_identity()

        # Check if the current user is an admin
        if not current_user['is_admin']:
            return jsonify({'error': 'You are not authorized to access this endpoint'}), 403

        # Query all employees from the database
        employees = Employee.query.all()

        serialized_employees = employees_schema.dump(employees)

        return jsonify({'employees': serialized_employees}), 200
    except Exception as e:
        return jsonify({'error': 'Internal Server Error'}), 500