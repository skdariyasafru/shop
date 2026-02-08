from flask import Flask, request, jsonify, redirect, session, render_template
from flask_login import LoginManager
from db import init_db, db
from db_init import create_tables
import os

from models.models import User, Product, Cart, Order

login_manager = LoginManager()
login_manager.login_view = "login"

def create_app():
app = Flask(**name**)
app.config["SECRET_KEY"] = "secret"

```
# =========================
# DATABASE SETUP
# =========================
init_db(app)
create_tables(app)

# =========================
# LOGIN MANAGER
# =========================
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# =========================
# HOME PAGE (LOAD PRODUCTS)
# =========================
@app.route("/")
def index():
    products = Product.query.all()
    user = session.get("user")  # logged-in username

    print("PRODUCTS:", products)  # DEBUG

    return render_template(
        "index.html",
        products=products,
        user=user
    )

# =========================
# GET PRODUCTS API
# =========================
@app.route("/products")
def get_products():
    products = Product.query.all()

    data = []
    for p in products:
        data.append({
            "id": p.id,
            "name": p.name,
            "price": p.price,
            "image": p.image
        })

    return jsonify(data)

# =========================
# REGISTER
# =========================
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        new_user = User(username=username, password=password)

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
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(
            username=username,
            password=password
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
    session.pop("user", None)
    return redirect("/")

# =========================
# ADD TO CART
# =========================
@app.route("/add_to_cart", methods=["POST"])
def add_to_cart():

    if "user" not in session:
        return jsonify({"msg": "login required"}), 401

    data = request.json

    item = Cart(
        username=session["user"],
        product_name=data["name"],
        price=data["price"]
    )

    db.session.add(item)
    db.session.commit()

    return jsonify({"msg": "added"})

# =========================
# VIEW CART
# =========================
@app.route("/cart")
def view_cart():

    if "user" not in session:
        return redirect("/login")

    items = Cart.query.filter_by(username=session["user"]).all()
    total = sum(i.price for i in items)

    return render_template(
        "cart.html",
        items=items,
        total=total
    )

# =========================
# CHECKOUT
# =========================
@app.route("/checkout")
def checkout():

    if "user" not in session:
        return redirect("/login")

    items = Cart.query.filter_by(username=session["user"]).all()

    for i in items:
        order = Order(
            user=i.username,
            product_name=i.product_name,
            price=i.price
        )
        db.session.add(order)
        db.session.delete(i)

    db.session.commit()

    return redirect("/")

return app
```

# =========================

# RUN APP

# =========================

app = create_app()

if **name** == "**main**":
port = int(os.environ.get("PORT", 10000))
app.run(host="0.0.0.0", port=port)
