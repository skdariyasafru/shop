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

       
        print("🚀 Migration finished safely")
