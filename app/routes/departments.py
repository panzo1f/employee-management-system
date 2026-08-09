from flask import Blueprint, flash, redirect, render_template, request, url_for

from app.services.department_service import DepartmentService


departments_bp = Blueprint(
    "departments",
    __name__,
    url_prefix="/departments",
)


@departments_bp.route("/")
def list_departments():
    departments = DepartmentService.get_all()

    return render_template(
        "departments/list.html",
        departments=departments,
    )


@departments_bp.route("/create", methods=["GET", "POST"])
def create_department():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        description = request.form.get("description", "").strip()

        if not name:
            flash("Department name is required.", "error")
            return render_template(
                "departments/create.html",
                name=name,
                description=description,
            )

        DepartmentService.create(
            name=name,
            description=description or None,
        )

        flash("Department created successfully.", "success")
        return redirect(url_for("departments.list_departments"))

    return render_template("departments/create.html")
