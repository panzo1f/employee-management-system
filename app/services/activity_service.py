from app.extensions import db
from app.models.activity import Activity


class ActivityService:

    @staticmethod
    def get_recent(limit=5):
        return (
            Activity.query
            .order_by(Activity.created_at.desc())
            .limit(limit)
            .all()
        )

    @staticmethod
    def create(action, description):
        activity = Activity(
            action=action,
            description=description,
        )

        db.session.add(activity)
        db.session.commit()

        return activity
