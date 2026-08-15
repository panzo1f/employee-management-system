from flask import Blueprint, render_template

from app.services.activity_service import ActivityService
from app.services.department_service import DepartmentService
from app.services.employee_service import EmployeeService
from app.services.user_service import UserService


dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/")
def index():
    employees = EmployeeService.get_all()
    departments = DepartmentService.get_all()
    statistics = EmployeeService.get_statistics()
    user_statistics = UserService.get_statistics()
    recent_activities = ActivityService.get_recent(5)

    return render_template(
        "dashboard/index.html",
        employees=employees,
        departments=departments,
        statistics=statistics,
        user_statistics=user_statistics,
        recent_activities=recent_activities,
    )
