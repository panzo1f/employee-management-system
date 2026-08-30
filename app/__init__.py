from flask import Flask

from app.core.config import Config
from app.extensions import db, migrate
from app.routes import register_blueprints
from app.services.translation_service import TranslationService
from app.services.user_preference_service import UserPreferenceService
from app.services.user_service import UserService


def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    # Import models so SQLAlchemy registers their tables
    from app import models

    register_blueprints(app)

    @app.context_processor
    def inject_user_preferences():
        users = UserService.get_all()

        if not users:
            return {
                "user_preferences": None,
                "language": "pt",
                "t": lambda key: TranslationService.translate(
                    key,
                    "pt",
                ),
            }

        preferences = UserPreferenceService.get_or_create(
            users[0].id
        )

        return {
            "user_preferences": preferences,
            "language": preferences.language,
            "t": lambda key: TranslationService.translate(
                key,
                preferences.language,
            ),
        }

    return app
