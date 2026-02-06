from db import db

def create_tables(app):
    with app.app_context():
        from models.models import User  # import all models here
        db.create_all()
        print("✅ Tables created successfully!")
