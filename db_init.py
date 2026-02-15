
from db import db

def create_tables(app):
    db.create_all()
