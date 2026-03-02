import os


class Config:
    # =====================================================
    # SECRET KEY (Always available)
    # =====================================================
    SECRET_KEY = "super-secret-production-key-2026"

    # =====================================================
    # DATABASE CONFIG
    # =====================================================

    # 1️⃣ First check environment variable (if exists)
    DATABASE_URL = os.environ.get("DATABASE_URL")

    # 2️⃣ If not found → use local SQLite
    if not DATABASE_URL:
        BASE_DIR = os.path.abspath(os.path.dirname(__file__))
        DATABASE_URL = "sqlite:///" + os.path.join(BASE_DIR, "database.db")

    # Fix old postgres:// issue
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace(
            "postgres://",
            "postgresql://",
            1
        )

    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # =====================================================
    # DATABASE PERFORMANCE SETTINGS
    # =====================================================
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_recycle": 300,
    }
