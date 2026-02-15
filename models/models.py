
from db import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(200))
    phone = db.Column(db.String(20))
    address = db.Column(db.Text)
    referral_code = db.Column(db.String(50))
    referred_by = db.Column(db.String(50))
    points = db.Column(db.Integer, default=0)


class Product(db.Model):
    __tablename__ = "product"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    price = db.Column(db.Float)
    image = db.Column(db.String(300))


class Cart(db.Model):
    __tablename__ = "cart"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    product_id = db.Column(db.Integer)
    quantity = db.Column(db.Integer, default=1)


class Order(db.Model):
    __tablename__ = "order"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    address = db.Column(db.Text)
    product_name = db.Column(db.String(200))
    price = db.Column(db.Float)
    quantity = db.Column(db.Integer)
    total = db.Column(db.Float)
    status = db.Column(db.String(50), default="Pending")
