from sqlalchemy import text
from db import db


def run_migration(app):
    with app.app_context():

        try:
            # Add username column to cart table if missing
            db.session.execute(text("""
                ALTER TABLE cart
                ADD COLUMN IF NOT EXISTS "username" VARCHAR(100);
            """))

            # Add username column to order table if missing
            db.session.execute(text("""
                ALTER TABLE "orders"
                ADD COLUMN IF NOT EXISTS "username" VARCHAR(100);
            """))

            db.session.commit()

            print("✅ Migration completed")

        except Exception as e:
            db.session.rollback()
            print("❌ Migration failed:", e)
