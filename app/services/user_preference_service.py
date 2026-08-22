from app.extensions import db
from app.models.user_preference import UserPreference


class UserPreferenceService:

    @staticmethod
    def get_by_user_id(user_id):
        return UserPreference.query.filter_by(
            user_id=user_id
        ).first()

    @staticmethod
    def get_or_create(user_id):
        preferences = UserPreferenceService.get_by_user_id(user_id)

        if preferences:
            return preferences

        preferences = UserPreference(
            user_id=user_id
        )

        db.session.add(preferences)
        db.session.commit()

        return preferences

    @staticmethod
    def update(
        user_id,
        theme,
        language,
        items_per_page,
        notifications_enabled,
    ):
        preferences = UserPreferenceService.get_or_create(user_id)

        preferences.theme = theme
        preferences.language = language
        preferences.items_per_page = items_per_page
        preferences.notifications_enabled = notifications_enabled

        db.session.commit()

        return preferences
