
import os

class Config:
    SECRET_KEY = "secretkey"
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "sqlite:///shop.db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
