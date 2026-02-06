from db import db

def create_tables(app):
    with app.app_context():
        from models.models import User  # import all models

        # Create tables only if they don't exist
        db.create_all()

        print("✅ Tables created if not exist (data safe)")
