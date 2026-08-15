from datetime import date

from app.extensions import db
from app.models.user import User
from app.services.activity_service import ActivityService


class UserService:

    @staticmethod
    def get_all():
        return User.query.order_by(User.id.desc()).all()

    @staticmethod
    def get_statistics():
        total = User.query.count()

        active = User.query.filter_by(is_active=True).count()

        today = date.today()

        new_this_month = User.query.filter(
            db.extract("year", User.created_at) == today.year,
            db.extract("month", User.created_at) == today.month,
        ).count()

        return {
            "total": total,
            "active": active,
            "new_this_month": new_this_month,
        }

    @staticmethod
    def create(name, email, is_active=True):
        user = User(
            name=name,
            email=email,
            is_active=is_active,
        )

        db.session.add(user)
        db.session.commit()

        ActivityService.create(
            "user_created",
            f"{user.name} foi criado",
        )

        return user
