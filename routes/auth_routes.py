
from flask import Blueprint, render_template, request, redirect, flash
from flask_login import login_user, logout_user, login_required
from db import db
from models.models import User, Product

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/")
def index():
    q = request.args.get("q")
    if q:
        products = Product.query.filter(Product.name.ilike(f"%{q}%")).all()
    else:
        products = Product.query.all()
    return render_template("index.html", products=products)

@auth_bp.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")
    user = User.query.filter_by(username=username).first()
    if not user or user.password != password:
        flash("Invalid login")
        return redirect("/?login=1")
    login_user(user)
    return redirect("/")

@auth_bp.route("/register", methods=["POST"])
def register():
    username = request.form.get("username")
    password = request.form.get("password")
    if User.query.filter_by(username=username).first():
        flash("User exists")
        return redirect("/?login=1")
    db.session.add(User(username=username, password=password))
    db.session.commit()
    flash("Registered successfully")
    return redirect("/?login=1")

@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")
