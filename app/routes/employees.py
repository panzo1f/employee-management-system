from datetime import datetime
from flask import Blueprint, flash, redirect, render_template, request, url_for
from sqlalchemy.exc import IntegrityError

from app.extensions import db
from app.services.department_service import DepartmentService
from app.services.employee_service import EmployeeService


employees_bp = Blueprint(
    "employees",
    __name__,
    url_prefix="/employees",
)


@employees_bp.route("/")
def list_employees():
    employees = EmployeeService.get_all()

    return render_template(
        "employees/list.html",
        employees=employees,
    )


@employees_bp.route("/create", methods=["GET", "POST"])
def create_employee():
    departments = DepartmentService.get_all()

    if request.method == "POST":
        first_name = request.form.get("first_name", "").strip()
        last_name = request.form.get("last_name", "").strip()
        email = request.form.get("email", "").strip()
        phone = request.form.get("phone", "").strip()
        position = request.form.get("position", "").strip()
        hire_date = request.form.get("hire_date", "").strip()
        salary = request.form.get("salary", "").strip()
        department_id = request.form.get("department_id", "").strip()

        if not first_name or not last_name:
            flash("First name and last name are required.", "error")

            return render_template(
                "employees/create.html",
                departments=departments,
                form=request.form,
            )

        if not email:
            flash("Email is required.", "error")

            return render_template(
                "employees/create.html",
                departments=departments,
                form=request.form,
            )

        if not position:
            flash("Position is required.", "error")

            return render_template(
                "employees/create.html",
                departments=departments,
                form=request.form,
            )

        if not hire_date:
            flash("Hire date is required.", "error")

            return render_template(
                "employees/create.html",
                departments=departments,
                form=request.form,
            )

        if not department_id:
            flash("Department is required.", "error")

            return render_template(
                "employees/create.html",
                departments=departments,
                form=request.form,
            )

        try:
            EmployeeService.create(
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone=phone or None,
                position=position,
                hire_date=hire_date,
                salary=salary or None,
                department_id=int(department_id),
            )

        except IntegrityError:
            db.session.rollback()

            flash(
                "This email is already registered.",
                "error",
            )

            return render_template(
                "employees/create.html",
                departments=departments,
                form=request.form,
            )

        flash("Employee created successfully.", "success")

        return redirect(
            url_for("employees.list_employees")
        )

    return render_template(
        "employees/create.html",
        departments=departments,
    )

@employees_bp.route("/<int:employee_id>")
def employee_details(employee_id):
    employee = EmployeeService.get_by_id(employee_id)

    if employee is None:
        flash("Employee not found.", "error")

        return redirect(
            url_for("employees.list_employees")
        )

    return render_template(
        "employees/details.html",
        employee=employee,
    )
@employees_bp.route("/<int:employee_id>/edit", methods=["GET", "POST"])
def edit_employee(employee_id):
    employee = EmployeeService.get_by_id(employee_id)

    if employee is None:
        flash("Employee not found.", "error")

        return redirect(
            url_for("employees.list_employees")
        )

    departments = DepartmentService.get_all()

    if request.method == "POST":
        first_name = request.form.get("first_name", "").strip()
        last_name = request.form.get("last_name", "").strip()
        email = request.form.get("email", "").strip()
        phone = request.form.get("phone", "").strip()
        position = request.form.get("position", "").strip()
        hire_date = request.form.get("hire_date", "").strip()
        salary = request.form.get("salary", "").strip()
        department_id = request.form.get("department_id", "").strip()

        if not all([
            first_name,
            last_name,
            email,
            position,
            hire_date,
            department_id,
        ]):
            flash("Please fill in all required fields.", "error")

            return render_template(
                "employees/edit.html",
                employee=employee,
                departments=departments,
            )


        hire_date = datetime.strptime(
            hire_date,
            "%Y-%m-%d",
        ).date()

        salary = salary or None

        EmployeeService.update(
            employee=employee,
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone or None,
            position=position,
            hire_date=hire_date,
            salary=salary,
            department_id=int(department_id),
        )

        flash("Employee updated successfully.", "success")

        return redirect(
            url_for(
                "employees.employee_details",
                employee_id=employee.id,
            )
        )

    return render_template(
        "employees/edit.html",
        employee=employee,
        departments=departments,
    )
@employees_bp.route("/<int:employee_id>/delete", methods=["POST"])
def delete_employee(employee_id):
    employee = EmployeeService.get_by_id(employee_id)

    if employee is None:
        flash("Employee not found.", "error")

        return redirect(
            url_for("employees.list_employees")
        )

    EmployeeService.delete(employee)

    flash("Employee deleted successfully.", "success")

    return redirect(
        url_for("employees.list_employees")
    )
