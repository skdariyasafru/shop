import os

class Config:
    SECRET_KEY = "supersecretkey"

    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        "postgresql://dariya:iXXzwPV9FQzQLqEUw35PJq9f3ItUT4rX@dpg-d5j4o50gjchc73cu2hsg-a/shop_aizq"
    )

    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
