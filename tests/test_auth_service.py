from app.services.auth_service import AuthService


def test_authenticate_valid_user(app):
    from app.models.user import User

    user = User.query.filter_by(
        email="admin@novahr.com"
    ).first()

    assert user is not None

    authenticated = AuthService.authenticate(
        "admin@novahr.com",
        "ChangeMe123!",
    )

    assert authenticated is not None
    assert authenticated.id == user.id


def test_authenticate_wrong_password(app):
    authenticated = AuthService.authenticate(
        "admin@novahr.com",
        "wrong-password",
    )

    assert authenticated is None


def test_authenticate_unknown_user(app):
    authenticated = AuthService.authenticate(
        "does-not-exist@novahr.com",
        "ChangeMe123!",
    )

    assert authenticated is None
