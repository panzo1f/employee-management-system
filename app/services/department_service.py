from app.extensions import db
from app.models.department import Department


class DepartmentService:

    @staticmethod
    def get_all():
        return Department.query.order_by(Department.id.desc()).all()

    @staticmethod
    def get_by_id(department_id):
        return db.session.get(Department, department_id)

    @staticmethod
    def create(name, description=None):
        department = Department(
            name=name,
            description=description,
        )

        db.session.add(department)
        db.session.commit()

        return department

    @staticmethod
    def update(department, name, description=None):
        department.name = name
        department.description = description

        db.session.commit()

        return department

    @staticmethod
    def delete(department):
        db.session.delete(department)
        db.session.commit()
