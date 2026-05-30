from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from models.models import User, Product
from db import db
import uuid

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/")
def home():
    return render_template("home.html")


@auth_bp.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        print("========== REGISTER ==========")
        print("FORM DATA:", request.form)

        username = request.form.get("username")
        password = generate_password_hash(
            request.form.get("password")
        )

        phone = request.form.get("phone")
        address = request.form.get("address")

        entered_code = request.form.get(
            "referred_by", ""
        ).strip()

        print("Entered Referral Code:", entered_code)

        referrer_id = 2

        if entered_code:

            referrer = User.query.filter_by(
                referral_code=entered_code
            ).first()

            print("Referrer Found:", referrer)

            if referrer:
                referrer_id = referrer.id
                print("Referrer ID:", referrer_id)

        new_referral_code = uuid.uuid4().hex[:8]

        print("New Referral Code:", new_referral_code)

        user = User(
            username=username,
            password=password,
            phone=phone,
            address=address,
            referral_code=new_referral_code,
            referred_by=2,
            wallet_balance=0,
            points=0
        )

        db.session.add(user)
        db.session.commit()

        print("Saved User ID:", user.id)
        print("Saved referred_by:", user.referred_by)
        print("=============================")
        saved_user = User.query.filter_by(username=username).first()

        print("Saved referred_by =", saved_user.referred_by)
        return redirect("/")

    return render_template("register.html")
@auth_bp.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for("auth.dashboard"))

        return redirect("/")

    return render_template("login.html")


@auth_bp.route("/dashboard")
@login_required
def dashboard():

    products = Product.query.all()

    return render_template(
        "dashboard.html",
        products=products
    )


@auth_bp.route("/logout")
@login_required
def logout():

    logout_user()

    return redirect(url_for("product.index"))
