from flask import Blueprint, render_template

from app.services.user_service import UserService


settings_bp = Blueprint("settings", __name__, url_prefix="/settings")


@settings_bp.route("/")
def index():
    return render_template("settings/index.html")


@settings_bp.route("/profile/")
def profile():
    users = UserService.get_all()

    user = users[0] if users else None

    return render_template(
        "settings/profile.html",
        user=user,
    )
