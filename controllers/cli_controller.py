from flask import Blueprint
from init import db, bcrypt
from models.employee import Employee

db_commands = Blueprint('db', __name__)

#auth_routes = Blueprint('auth', __name__, url_prefix="/auth/")
#@auth_routes.route("/register")

@db_commands.cli.command('create')
def create_db():
    db.create_all()
    print("Tables Created")
    
@db_commands.cli.command('drop')
def drop_db():
    db.drop_all()
    print("Tables dropped")
    
@db_commands.cli.command('seed')
def seed_db():
    employees = [
        Employee(
            employee_name='Kim Perez',
            employee_email="kimperez@admin.com",
            password=bcrypt.generate_password_hash('adminpw').decode('utf-8'),
            is_admin=True
        ),
        Employee(
            employee_name='Leo Dicaprio',
            employee_email="leodicaprio@email.com",
            password=bcrypt.generate_password_hash('employee1pw').decode('utf-8')
        )
    ]
    
    db.session.add_all(employees)
    db.session.commit()
    
    print("Tables seeded")