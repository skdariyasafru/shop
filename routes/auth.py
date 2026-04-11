from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models.models import User, Product
from db import db
import uuid

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/")
def home():
    return render_template("home.html")


# ================= REGISTER =================
@auth_bp.route("/register", methods=["POST"])
def register():
    username = request.form["username"]
    password = generate_password_hash(request.form["password"])

    phone = request.form.get("phone")
    address = request.form.get("address")

    referral_code = request.form.get("referral_code")

    # 🔍 Find referrer
    referrer = None
    if referral_code:
        referrer = User.query.filter_by(referral_code=referral_code).first()

    # 🚫 Duplicate user
    if User.query.filter_by(username=username).first():
        return redirect(url_for("auth.home", register=1))

    # 🎯 Generate new referral code
    import uuid
    new_ref_code = str(uuid.uuid4())[:8]

    # ✅ CREATE USER
    user = User(
        username=username,
        password=password,
        phone=phone,
        address=address,
        referral_code=new_ref_code,
        referred_by=referrer.id if referrer else None
    )

    db.session.add(user)
    db.session.commit()

    return redirect(url_for("auth.home", login=1))
# ================= LOGIN =================
@auth_bp.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    user = User.query.filter_by(username=username).first()

    if user and check_password_hash(user.password, password):
        login_user(user)
        return redirect(url_for("auth.dashboard"))

    return redirect(url_for("auth.home", login=1))


# ================= DASHBOARD =================
@auth_bp.route("/dashboard")
@login_required
def dashboard():
    products = Product.query.all()

    referral_link = request.host_url + "?ref=" + current_user.referral_code

    return render_template(
        "dashboard.html",
        products=products,
        referral_link=referral_link
    )


# ================= LOGOUT =================
@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.home"))
