import uuid
from flask import Blueprint, request, redirect, flash
from flask_login import login_user, logout_user, login_required
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

    username = request.form.get("username")
    password = request.form.get("password")
    phone = request.form.get("phone")
    address = request.form.get("address")

    if User.query.filter_by(username=username).first():
        flash("User already exists")
        return redirect("/?login=1")

    new_user = User(
        username=username,
        password=password,
        phone=phone,
        address=address,
        referral_code=str(uuid.uuid4())[:8],
        points=0
    )

    db.session.add(new_user)
    db.session.commit()

    flash("Registration successful")

    return redirect("/?login=1")


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out")
    return redirect("/")