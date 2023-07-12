from flask import Blueprint, request
from init import db, bcrypt
from models.employee import Employee, employee_schema, employees_schema
from flask_jwt_extended import create_access_token
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes

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