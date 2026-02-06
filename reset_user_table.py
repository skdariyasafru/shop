from db import db

def reset_user_table(app):
    with app.app_context():
        from models.models import User

        # Drop only User table if exists
        User.__table__.drop(db.engine, checkfirst=True)

        # Recreate User table
        User.__table__.create(db.engine)

        print("✅ User table deleted and recreated!")
