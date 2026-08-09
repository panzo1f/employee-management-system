from datetime import datetime

from app.extensions import db


class Employee(db.Model):
    __tablename__ = "employees"

    id = db.Column(db.Integer, primary_key=True)

    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)

    email = db.Column(db.String(150), nullable=False, unique=True)
    phone = db.Column(db.String(30), nullable=True)

    position = db.Column(db.String(100), nullable=False)

    hire_date = db.Column(db.Date, nullable=False)
    salary = db.Column(db.Numeric(12, 2), nullable=True)

    department_id = db.Column(
        db.Integer,
        db.ForeignKey("departments.id"),
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    department = db.relationship(
        "Department",
        backref="employees"
    )

    def __repr__(self):
        return f"<Employee {self.first_name} {self.last_name}>"
