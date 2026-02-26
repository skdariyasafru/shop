from datetime import datetime
from flask_login import UserMixin
from db import db


# ================= USER =================
class User(UserMixin, db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)

    # Indexed for faster login search
    username = db.Column(db.String(100), unique=True, index=True)

    password = db.Column(db.String(200))

    phone = db.Column(db.String(20))
    address = db.Column(db.Text)

    referral_code = db.Column(db.String(50), index=True)
    referred_by = db.Column(db.String(50), index=True)

    points = db.Column(db.Integer, default=0)

    # Relationship (faster access to user cart)
    carts = db.relationship("Cart", backref="user", lazy=True)



# ================= PRODUCT =================
class Product(db.Model):
    __tablename__ = "product"

    id = db.Column(db.Integer, primary_key=True)

    # INDEX ADDED → makes search very fast
    name = db.Column(db.String(200), index=True)

    price = db.Column(db.Float)
    image = db.Column(db.String(300))

    # Relationship (optional but good practice)
    carts = db.relationship("Cart", backref="product", lazy=True)



# ================= CART =================
class Cart(db.Model):
    __tablename__ = "cart"

    id = db.Column(db.Integer, primary_key=True)

    # Foreign Keys (important for performance + integrity)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), index=True)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), index=True)

    quantity = db.Column(db.Integer, default=1)



# ================= ORDER =================
class Order(db.Model):
    __tablename__ = "order"

    id = db.Column(db.Integer, primary_key=True)

    order_number = db.Column(db.String(20), unique=True, index=True)

    username = db.Column(db.String(100), index=True)

    phone = db.Column(db.String(20))
    address = db.Column(db.Text)

    product_name = db.Column(db.String(200))
    price = db.Column(db.Float)
    quantity = db.Column(db.Integer)
    total = db.Column(db.Float)

    payment_method = db.Column(db.String(50), default="COD")
    payment_status = db.Column(db.String(50), default="Pending")

    status = db.Column(db.String(50), default="Pending")

    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
