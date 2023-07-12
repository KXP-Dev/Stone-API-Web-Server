from init import db, ma

class Employee(db.Model):
    __tablename__ = 'employees'
    
    employee_id = db.Column(db.Integer, primary_key=True)
    employee_name = db.Column(db.String)
    employee_email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    
class EmployeeSchema(ma.Schema):
    class Meta:
        fields = ('employee_id', 'employee_name', 'employee_email', 'password', 'is_admin')
        
employee_schema = EmployeeSchema(exclude=['password'])
employees_schema = EmployeeSchema(many=True, exclude=['password'])