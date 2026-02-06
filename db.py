from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://dariya:iXXzwPV9FQzQLqEUw35PJq9f3ItUT4rX@dpg-d5j4o50gjchc73cu2hsg-a/shop_aizq"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

   
