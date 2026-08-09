import os


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")

    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg://novahr:novahr_password@localhost:5432/novahr"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False
