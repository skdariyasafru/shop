import os


class Config:

    # SECRET KEY
    SECRET_KEY = os.environ.get(
        "SECRET_KEY",
        "super-secret-production-key-2026"
    )

    # DATABASE URL from environment
    DATABASE_URL = os.environ.get("DATABASE_URL")

    # If no external DB → use local SQLite
    if not DATABASE_URL:
        BASE_DIR = os.path.abspath(os.path.dirname(__file__))
        DATABASE_URL = "sqlite:///" + os.path.join(BASE_DIR, "database.db")

    # Render / Heroku compatibility fix
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace(
            "postgres://",
            "postgresql://",
            1
        )

    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Safe connection pooling for Render
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_recycle": 300,
        "pool_size": 5,
        "max_overflow": 2
    }
