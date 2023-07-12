from flask import Blueprint, request
from init import db, bcrypt
from models.employee import Employee, employee_schema, employees_schema
from flask_jwt_extended import create_access_token
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes
from datetime import timedelta

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['POST'])
def auth_register():
    try:
        body_data = request.get_json() #{"employee_name": "Brad Pitt","employee_email": "bradpitt@email.com","password": "employee2pw"}
        
        # Create a new Employee model instance from the user info.
        employee = Employee() # Instance of the Employee class which is in turn a SQLAlchemy model.
        employee.employee_name = body_data.get('employee_name')
        employee.employee_email = body_data.get('employee_email')
        employee.password = bcrypt.generate_password_hash(body_data.get('password')).decode('utf-8')
        # Add the employee to the session.
        db.session.add(employee)
        # Commit to add the employee to the database.
        db.session.commit()
        # Respond to the client.
        return employee_schema.dump(employee), 201
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return { 'error': 'Email address already in use' }, 409
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return { 'error': f'The {err.orig.diag.column_name} is required' }, 409
        
@auth_bp.route('/login', methods=['POST'])
def auth_login():
    body_data = request.get_json()
    # Find the user by email address
    stmt = db.select(Employee).filter_by(employee_email=body_data.get('employee_email'))
    employee = db.session.scalar(stmt)
    # If employee exists and password is correct
    if employee and bcrypt.check_password_hash(employee.password, body_data.get('password')):
        token = create_access_token(identity=str(employee.employee_id), expires_delta=timedelta(days=1))
        return { 'employee_email': employee.employee_email, 'token': token, 'is_admin': employee.is_admin }
    else:
        return { 'error': 'Invalid email or password' }, 401