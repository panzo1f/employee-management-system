from app.extensions import db


class UserPreference(db.Model):
    __tablename__ = "user_preferences"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
        unique=True
    )

    theme = db.Column(
        db.String(20),
        nullable=False,
        default="light"
    )

    language = db.Column(
        db.String(10),
        nullable=False,
        default="pt"
    )

    items_per_page = db.Column(
        db.Integer,
        nullable=False,
        default=10
    )

    notifications_enabled = db.Column(
        db.Boolean,
        nullable=False,
        default=True
    )

    user = db.relationship(
        "User",
        backref=db.backref(
            "preferences",
            uselist=False
        )
    )

    def __repr__(self):
        return f"<UserPreference user_id={self.user_id}>"
