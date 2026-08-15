from datetime import date

from app.extensions import db
from app.models.employee import Employee


class EmployeeService:

    @staticmethod
    def get_all(search=None, status=None):
        query = Employee.query

        if search:
            search = search.strip()

            if search:
                search_pattern = f"%{search}%"

                query = query.filter(
                    db.or_(
                        Employee.first_name.ilike(search_pattern),
                        Employee.last_name.ilike(search_pattern),
                        Employee.email.ilike(search_pattern),
                    )
                )

        if status == "active":
            query = query.filter(Employee.is_active.is_(True))

        elif status == "inactive":
            query = query.filter(Employee.is_active.is_(False))

        return query.order_by(Employee.id.desc()).all()

    @staticmethod
    def get_by_id(employee_id):
        return db.session.get(Employee, employee_id)

    @staticmethod
    def get_statistics():
        total = Employee.query.count()

        active = Employee.query.filter_by(is_active=True).count()

        active_percentage = (
            (active / total) * 100
            if total > 0
            else 0
        )

        today = date.today()

        new_this_month = Employee.query.filter(
            db.extract("year", Employee.hire_date) == today.year,
            db.extract("month", Employee.hire_date) == today.month,
        ).count()

        return {
            "total": total,
            "active": active,
            "active_percentage": active_percentage,
            "new_this_month": new_this_month,
        }

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
        is_active=True,
    ):
        employee.first_name = first_name
        employee.last_name = last_name
        employee.email = email
        employee.phone = phone
        employee.position = position
        employee.hire_date = hire_date
        employee.salary = salary
        employee.department_id = department_id
        employee.is_active = is_active

        db.session.commit()

        return employee

    @staticmethod
    def delete(employee):
        db.session.delete(employee)
        db.session.commit()
