from werkzeug.security import check_password_hash

from app.models.user import User


class AuthService:

    @staticmethod
    def authenticate(email, password):
        user = User.query.filter_by(email=email).first()

        if user is None:
            return None

        if not user.is_active:
            return None

        if not check_password_hash(
            user.password_hash,
            password,
        ):
            return None

        return user
