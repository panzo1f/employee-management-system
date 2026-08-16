from flask import Blueprint, render_template

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
