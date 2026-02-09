from flask import Flask, request, jsonify, redirect, session, render_template
from flask_login import LoginManager
from db import init_db, db
from db_init import create_tables
import os

from models.models import User, Product, Cart, Order

login_manager = LoginManager()
login_manager.login_view = "login"

def create_app():
app = Flask(__name__)
app.config["SECRET_KEY"] = "secret"

 
# =========================
# DATABASE SETUP
# =========================
init_db(app)

with app.app_context():
    create_tables(app)

# =========================
# LOGIN MANAGER
# =========================
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# =========================
# HOME PAGE
# =========================
@app.route("/")
def index():
    category = request.args.get("category")

    if category:
        products = Product.query.filter_by(category=category).all()
    else:
        products = Product.query.all()

    return render_template(
        "index.html",
        products=products,
        user=session.get("user")
    )

# =========================
# REGISTER
# =========================
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        new_user = User(
            username=request.form.get("username"),
            password=request.form.get("password")
        )

        db.session.add(new_user)
        db.session.commit()

        return redirect("/login")

    return render_template("register.html")

# =========================
# LOGIN
# =========================
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = User.query.filter_by(
            username=request.form.get("username"),
            password=request.form.get("password")
        ).first()

        if user:
            session["user"] = user.username
            return redirect("/")

        return "Invalid login"

    return render_template("login.html")

# =========================
# LOGOUT
# =========================
@app.route("/logout")
def logout():
    sessio
 
