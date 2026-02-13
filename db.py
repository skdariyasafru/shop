from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:Shaik09871234@db.ujlsspolbtusivmilioh.supabase.co:5432/postgres?sslmode=require
"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

   
