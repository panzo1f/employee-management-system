from app.extensions import db
from app.models.employee import Employee


class EmployeeService:

    @staticmethod
    def get_all():
        return Employee.query.order_by(Employee.id.desc()).all()

    @staticmethod
    def get_by_id(employee_id):
        return db.session.get(Employee, employee_id)

    @staticmethod
    def create(
        first_name,
        last_name,
        email,
        position,
        hire_date,
        department_id,
        phone=None,
        salary=None,
    ):
        employee = Employee(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            position=position,
            hire_date=hire_date,
            salary=salary,
            department_id=department_id,
        )

        db.session.add(employee)
        db.session.commit()

        return employee

    @staticmethod
    def update(
        employee,
        first_name,
        last_name,
        email,
        position,
        hire_date,
        department_id,
        phone=None,
        salary=None,
    ):
        employee.first_name = first_name
        employee.last_name = last_name
        employee.email = email
        employee.phone = phone
        employee.position = position
        employee.hire_date = hire_date
        employee.salary = salary
        employee.department_id = department_id

        db.session.commit()

        return employee

    @staticmethod
    def delete(employee):
        db.session.delete(employee)
        db.session.commit()
