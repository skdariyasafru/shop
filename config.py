import os


class Config:

    # ================= SECRET KEY =================
    # MUST set in Render environment variables
    SECRET_KEY = os.environ.get("SECRET_KEY")

    if not SECRET_KEY:
        raise RuntimeError("SECRET_KEY not set in environment variables")

    # ================= DATABASE =================
    DATABASE_URL = os.environ.get("DATABASE_URL")

    if not DATABASE_URL:
        raise RuntimeError("DATABASE_URL not set in environment variables")

    # Fix old postgres:// issue
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace(
            "postgres://",
            "postgresql://",
            1
        )

    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # ================= CONNECTION POOL =================
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,      # Prevent stale connections
        "pool_recycle": 1800,       # Recycle every 30 mins
        "pool_size": 5,
        "max_overflow": 10,
        "pool_timeout": 30,
    }

    # ================= SESSION SETTINGS =================
    # Required for Render HTTPS
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
