import os


class Config:

    # ================= SECRET KEY =================
    SECRET_KEY = os.environ.get(
        "SECRET_KEY",
        "super-secret-production-key"
    )

    # ================= DATABASE URL =================
    DATABASE_URL = os.environ.get("DATABASE_URL")

    # fallback to sqlite for local development
    if not DATABASE_URL:
        BASE_DIR = os.path.abspath(os.path.dirname(__file__))
        DATABASE_URL = "sqlite:///" + os.path.join(BASE_DIR, "database.db")

    # Render / Heroku fix
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace(
            "postgres://",
            "postgresql://",
            1
        )

    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # ================= SQLALCHEMY SETTINGS =================
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_recycle": 280,
        "pool_size": 5,
        "max_overflow": 10,
        "connect_args": {
            "sslmode": "require"   # important for Supabase
        }
    }
