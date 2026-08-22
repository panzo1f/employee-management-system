from flask import Blueprint, redirect, render_template, request, session, url_for

from app.services.auth_service import AuthService


auth_bp = Blueprint(
    "auth",
    __name__,
)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        user = AuthService.authenticate(
            email,
            password,
        )

        if user is None:
            return render_template(
                "auth/login.html",
                error="Invalid email or password.",
                email=email,
            )

        session.clear()

        session["user_id"] = user.id
        session["user_name"] = user.name
        session["user_email"] = user.email

        return redirect(
            url_for("dashboard.index")
        )

    return render_template(
        "auth/login.html"
    )


@auth_bp.route("/logout", methods=["POST"])
def logout():
    session.clear()

    return redirect(
        url_for("auth.login")
    )
