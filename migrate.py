from sqlalchemy import text
from db import db


def safe_execute(sql):
    try:
        db.session.execute(text(sql))
        db.session.commit()
        print("✅ OK:", sql.split()[2])
    except Exception as e:
        db.session.rollback()
        print("⚠️ Skipped:", e)


def run_migration(app):
    with app.app_context():

        # CART TABLE
        safe_execute("""
            ALTER TABLE cart
            ADD COLUMN IF NOT EXISTS username VARCHAR(100);
        """)

        safe_execute("""
            ALTER TABLE cart
            ADD COLUMN IF NOT EXISTS product_name VARCHAR(200);
        """)

        safe_execute("""
            ALTER TABLE cart
            ADD COLUMN IF NOT EXISTS price FLOAT;
        """)

        # ORDER TABLE
        safe_execute("""
            ALTER TABLE "order"
            ADD COLUMN IF NOT EXISTS username VARCHAR(100);
        """)

        safe_execute("""
            ALTER TABLE "order"
            ADD COLUMN IF NOT EXISTS product_name VARCHAR(200);
        """)

        safe_execute("""
            ALTER TABLE "order"
            ADD COLUMN IF NOT EXISTS price FLOAT;
        """)

        print("🚀 Migration finished safely")
