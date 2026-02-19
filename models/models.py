from datetime import datetime
from db import db
from flask_login import UserMixin


# ================= USER =================

class User(UserMixin, db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    phone = db.Column(db.String(20))
    address = db.Column(db.Text)

    referral_code = db.Column(db.String(50), unique=True)
    referred_by = db.Column(db.String(50))

    # 🔥 MLM SYSTEM FIELDS
    points = db.Column(db.Integer, default=0)
    pv = db.Column(db.Float, default=0)        # Personal Volume
    wallet = db.Column(db.Float, default=0)    # Wallet balance

    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# ================= PRODUCT =================

class Product(db.Model):
    __tablename__ = "product"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(300))

    # Optional PV per product
    pv_value = db.Column(db.Float, default=0)


# ================= CART =================

class Cart(db.Model):
    __tablename__ = "cart"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, nullable=False)
    product_id = db.Column(db.Integer, nullable=False)

    quantity = db.Column(db.Integer, default=1)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# ================= ORDER =================

class Order(db.Model):
    __tablename__ = "order"

    id = db.Column(db.Integer, primary_key=True)

    # 🔥 Unique Order Number (group multiple products)
    order_number = db.Column(db.String(20), index=True)

    username = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    address = db.Column(db.Text)

    product_name = db.Column(db.String(200))
    price = db.Column(db.Float)
    quantity = db.Column(db.Integer)
    total = db.Column(db.Float)

    payment_method = db.Column(db.String(50), default="COD")
    payment_status = db.Column(db.String(50), default="Pending")

    status = db.Column(db.String(50), default="Pending")

    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# ================= WALLET TRANSACTIONS =================

class WalletTransaction(db.Model):
    __tablename__ = "wallet_transaction"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer)
    amount = db.Column(db.Float)
    type = db.Column(db.String(50))  # Credit / Debit
    description = db.Column(db.String(200))

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
