from flask import Blueprint, flash, redirect, render_template, request, url_for

from app.services.user_service import UserService


users_bp = Blueprint(
    "users",
    __name__,
    url_prefix="/users",
)


@users_bp.route("/")
def list_users():
    users = UserService.get_all()

    return render_template(
        "users/list.html",
        users=users,
    )


@users_bp.route("/create", methods=["GET", "POST"])
def create_user():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        is_active = request.form.get("is_active") == "on"

        if not name:
            flash("User name is required.", "error")

            return render_template(
                "users/create.html",
                name=name,
                email=email,
                is_active=is_active,
            )

        if not email:
            flash("User email is required.", "error")

            return render_template(
                "users/create.html",
                name=name,
                email=email,
                is_active=is_active,
            )

        UserService.create(
            name=name,
            email=email,
            is_active=is_active,
        )

        flash("User created successfully.", "success")

        return redirect(
            url_for("users.list_users")
        )

    return render_template(
        "users/create.html",
        is_active=True,
    )

@users_bp.route(
    "/<int:user_id>/edit",
    methods=["GET", "POST"],
)
def edit_user(user_id):
    user = UserService.get_by_id(user_id)

    if user is None:
        flash("User not found.", "error")

        return redirect(
            url_for("users.list_users")
        )

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        is_active = request.form.get("is_active") == "on"

        if not name:
            flash("User name is required.", "error")

            return render_template(
                "users/edit.html",
                user=user,
            )

        if not email:
            flash("User email is required.", "error")

            return render_template(
                "users/edit.html",
                user=user,
            )

        UserService.update(
            user=user,
            name=name,
            email=email,
            is_active=is_active,
        )

        flash("User updated successfully.", "success")

        return redirect(
            url_for("users.list_users")
        )

    return render_template(
        "users/edit.html",
        user=user,
    )
