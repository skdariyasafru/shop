from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from models.models import User, Product
from db import db
import uuid

auth_bp = Blueprint("auth", __name__)


# 🏠 Home Page
@auth_bp.route("/")
def home():
    return render_template("home.html")


# 📝 Register Page (WITH REFERRAL SUPPORT)
@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = generate_password_hash(request.form["password"])

        # 🔗 Get referral code from form
        referral_code = request.form.get("referral_code")

        referrer = None
        if referral_code:
            referrer = User.query.filter_by(referral_code=referral_code).first()

        # 🚫 Prevent duplicate users
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return "User already exists"

        # 🎯 Generate unique referral code
        new_ref_code = str(uuid.uuid4())[:8]

        # 👤 Create new user
        user = User(
            username=username,
            password=password,
            referral_code=new_ref_code,
            referred_by=referrer.id if referrer else None,
            wallet_balance=0.0
        )

        db.session.add(user)
        db.session.commit()

        return redirect(url_for("auth.login"))

    # 🔗 Capture referral from URL (?ref=XXXX)
    ref = request.args.get("ref")

    return render_template("register.html", ref=ref)


# 🔐 Login Page
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for("auth.dashboard"))

        return "Invalid username or password"

    return render_template("login.html")


# 📊 Dashboard
@auth_bp.route("/dashboard")
@login_required
def dashboard():
    products = Product.query.all()

    # 🔗 Create referral link for logged-in user
    referral_link = request.host_url + "register?ref=" + current_user.referral_code

    return render_template(
        "dashboard.html",
        products=products,
        referral_link=referral_link
    )


# 🚪 Logout
@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
