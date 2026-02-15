
from db import db

def create_tables(app):
    with app.app_context():
        db.create_all()
