import os

class Config:
    SECRET_KEY = "supersecretkey"

    DATABASE_URL = os.getenv("DATABASE_URL")

    # Render postgres fix
    if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace(
            "postgres://", "postgresql://", 1
        )

    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
