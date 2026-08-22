from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)

from app.services.user_preference_service import UserPreferenceService
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


@settings_bp.route("/preferences/", methods=["GET", "POST"])
def preferences():
    users = UserService.get_all()

    user = users[0] if users else None

    if not user:
        return render_template(
            "settings/preferences.html",
            user=None,
            preferences=None,
        )

    preferences = UserPreferenceService.get_or_create(user.id)

    if request.method == "POST":
        theme = request.form.get("theme")
        language = request.form.get("language")
        items_per_page = request.form.get("items_per_page")
        notifications_enabled = request.form.get("notifications_enabled")

        UserPreferenceService.update(
            user.id,
            theme,
            language,
            int(items_per_page),
            notifications_enabled == "on",
        )

        flash(
            "Preferências atualizadas com sucesso.",
            "success",
        )

        return redirect(url_for("settings.preferences"))

    return render_template(
        "settings/preferences.html",
        user=user,
        preferences=preferences,
    )