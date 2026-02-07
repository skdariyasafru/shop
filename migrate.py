from sqlalchemy import text
from db import db


def run_migration(app):
    with app.app_context():

       
        

      

        db.session.execute(text("""
            ALTER TABLE cart
            ADD COLUMN IF NOT EXISTS price FLOAT;
        """))

        db.session.execute(text("""
            ALTER TABLE "order"
            ADD COLUMN IF NOT EXISTS product_name VARCHAR(200);
        """))

        db.session.execute(text("""
            ALTER TABLE "order"
            ADD COLUMN IF NOT EXISTS price FLOAT;
        """))

        db.session.commit()

        print("✅ Migration completed (username fix)")
