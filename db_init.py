from db import db
from sqlalchemy import text


def create_tables(app):
    with app.app_context():

        # Create tables if not exist
        db.create_all()

        # Auto add missing column (migration)
        try:
            db.session.execute(
                text("ALTER TABLE cart ADD COLUMN quantity INTEGER DEFAULT 1")
            )
            db.session.commit()
            print("✅ Migration applied: quantity column added")

        except Exception:
            db.session.rollback()
            print("✔ Column already exists, skipping migration")
