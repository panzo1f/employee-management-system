from app.extensions import db
from app.models.activity import Activity
from app.models.department import Department
from app.models.employee import Employee
from app.models.user import User


class ReportService:

    @staticmethod
    def get_summary():
        total_employees = Employee.query.count()

        active_employees = Employee.query.filter(
            Employee.is_active.is_(True)
        ).count()

        total_departments = Department.query.count()

        total_users = User.query.count()

        return {
            "total_employees": total_employees,
            "active_employees": active_employees,
            "total_departments": total_departments,
            "total_users": total_users,
        }

    @staticmethod
    def get_employees_by_department():
        results = (
            db.session.query(
                Department.name,
                db.func.count(Employee.id),
            )
            .outerjoin(
                Employee,
                Employee.department_id == Department.id,
            )
            .group_by(Department.id, Department.name)
            .order_by(db.func.count(Employee.id).desc())
            .all()
        )

        return [
            {
                "name": name,
                "count": count,
            }
            for name, count in results
        ]

    @staticmethod
    def get_employee_status():
        active = Employee.query.filter(
            Employee.is_active.is_(True)
        ).count()

        inactive = Employee.query.filter(
            Employee.is_active.is_(False)
        ).count()

        return {
            "active": active,
            "inactive": inactive,
        }

    @staticmethod
    def get_hiring_trend():
        results = (
            db.session.query(
                db.extract("year", Employee.hire_date).label("year"),
                db.extract("month", Employee.hire_date).label("month"),
                db.func.count(Employee.id).label("count"),
            )
            .group_by(
                db.extract("year", Employee.hire_date),
                db.extract("month", Employee.hire_date),
            )
            .order_by(
                db.extract("year", Employee.hire_date),
                db.extract("month", Employee.hire_date),
            )
            .all()
        )

        return [
            {
                "year": int(year),
                "month": int(month),
                "count": count,
            }
            for year, month, count in results
        ]

    @staticmethod
    def get_employees_by_position():
        results = (
            db.session.query(
                Employee.position,
                db.func.count(Employee.id),
            )
            .group_by(Employee.position)
            .order_by(db.func.count(Employee.id).desc())
            .all()
        )

        return [
            {
                "position": position,
                "count": count,
            }
            for position, count in results
        ]

    @staticmethod
    def get_system_activity():
        created = Activity.query.filter(
            Activity.action.in_([
                "employee_created",
                "user_created",
            ])
        ).count()

        updated = Activity.query.filter(
            Activity.action == "user_updated"
        ).count()

        deleted = Activity.query.filter(
            Activity.action == "user_deleted"
        ).count()

        return {
            "created": created,
            "updated": updated,
            "deleted": deleted,
        }

    @staticmethod
    def get_dashboard_data():
        return {
            "summary": ReportService.get_summary(),
            "employees_by_department": (
                ReportService.get_employees_by_department()
            ),
            "employee_status": (
                ReportService.get_employee_status()
            ),
            "hiring_trend": (
                ReportService.get_hiring_trend()
            ),
            "employees_by_position": (
                ReportService.get_employees_by_position()
            ),
            "system_activity": (
                ReportService.get_system_activity()
            ),
        }
