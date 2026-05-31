import uuid

from flask import Blueprint, request, redirect, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash

from models.models import User
from db import db

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["POST"])
def login():

    username = request.form.get("username")
    password = request.form.get("password")

    user = User.query.filter_by(username=username).first()

    if not user or user.password != password:
        flash("Invalid credentials")
        return redirect("/?login=1")

    login_user(user)

    flash("Login successful")

    return redirect("/")


@auth_bp.route("/register", methods=["POST"])
def register():

    print("========== REGISTER ==========")
    print("FORM DATA:", request.form)

    username = request.form.get("username")
    password = password = request.form.get("password")
    phone = request.form.get("phone")
    address = request.form.get("address")

    entered_code = request.form.get(
        "referred_by", ""
    ).strip()

    print("Entered Referral Code:", entered_code)

    referrer_id = 1

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
        referred_by=referrer_id,
        points=0
    )

    db.session.add(user)
    db.session.commit()

    saved_user = User.query.filter_by(
        username=username
    ).first()

    print("Saved User ID:", saved_user.id)
    print("Saved referred_by:", saved_user.referred_by)

    flash("Registration successful")

    return redirect("/")


@auth_bp.route("/logout")
@login_required
def logout():

    logout_user()

    flash("Logged out")

    return redirect("/")
