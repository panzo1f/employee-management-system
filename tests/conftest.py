import os

import pytest

from app import create_app
from app.extensions import db
from app.models.user import User
from werkzeug.security import generate_password_hash


@pytest.fixture
def app():
    app = create_app()

    app.config.update(
        TESTING=True,
        SQLALCHEMY_DATABASE_URI=os.getenv(
            "DATABASE_URL",
            "postgresql+psycopg://novahr:novahr_password@localhost:5432/novahr_test",
        ),
        SECRET_KEY="test-secret-key",
    )

    with app.app_context():
        db.drop_all()
        db.create_all()

        test_user = User(
            name="Pedro Admin",
            email="admin@novahr.com",
            password_hash=generate_password_hash(
                "ChangeMe123!"
            ),
            is_active=True,
        )

        db.session.add(test_user)
        db.session.commit()

        yield app

        db.session.remove()
        db.drop_all()
