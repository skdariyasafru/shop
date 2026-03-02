import os


class Config:
    # =====================================================
    # SECRET KEY (Safe for Render + Local)
    # =====================================================
    SECRET_KEY = os.environ.get(
        "SECRET_KEY",
        "dev-secret-key-change-in-production"
    )

    # =====================================================
    # DATABASE CONFIGURATION
    # =====================================================
    DATABASE_URL = os.environ.get("DATABASE_URL")

    # Fix old postgres:// issue (Render compatibility)
    if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace(
            "postgres://",
            "postgresql://",
            1
        )

    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # =====================================================
    # SQLAlchemy Performance Options (Safe Defaults)
    # =====================================================
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_recycle": 300,
    }
