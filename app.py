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


init_db(app)

with app.app_context():
    create_tables(app)

login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/")
def index():
    products = Product.query.all()
    return render_template("index.html", products=products, user=session.get("user"))

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

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/")

@app.route("/add_to_cart", methods=["POST"])
def add_to_cart():
    if "user" not in session:
        return jsonify({"msg": "login required"}), 401

    data = request.json
    username = session["user"]

    item = Cart.query.filter_by(username=username, product_name=data["name"]).first()

    if item:
        item.quantity += 1
    else:
        db.session.add(Cart(
            username=username,
            product_name=data["name"],
            price=data["price"],
            quantity=1
        ))

    db.session.commit()
    return jsonify({"msg": "added"})

@app.route("/cart")
def cart():
    if "user" not in session:
        return redirect("/login")

    items = Cart.query.filter_by(username=session["user"]).all()
    total = sum(i.price * i.quantity for i in items)

    return render_template("cart.html", items=items, total=total)

return app


app = create_app()

if __name__ == "__main__":
port = int(os.environ.get("PORT", 10000))
app.run(host="0.0.0.0", port=port)
