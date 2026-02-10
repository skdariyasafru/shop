from flask import Flask, request, jsonify, redirect, render_template, session
from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    login_required,
    current_user
)
from datetime import timedelta
import os

from db import init_db, db
from db_init import create_tables
from models.models import User, Product, Cart, Order


def seed_products():
    """Add sample products if database is empty"""
    if Product.query.count() == 0:
        print("Seeding sample products...")

        products = [
            Product(name="Phone", price=15000, image="https://via.placeholder.com/200"),
            Product(name="Laptop", price=50000, image="https://via.placeholder.com/200"),
            Product(name="Headphones", price=2000, image="https://via.placeholder.com/200"),
        ]

        db.session.add_all(products)
        db.session.commit()


def create_app():
    app = Flask(__name__)

    # ================= CONFIG =================
    app.config["SECRET_KEY"] = "super-secret-key-change-this"
    app.config["SESSION_COOKIE_SECURE"] = False
    app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
    app.permanent_session_lifetime = timedelta(days=1)

    # ================= DATABASE =================
    init_db(app)

    with app.app_context():
        create_tables(app)
        seed_products()  # 👈 auto add products

    # ================= LOGIN MANAGER =================
    login_manager = LoginManager()
    login_manager.login_view = "login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # ================= DEBUG ROUTE =================
    @app.route("/testdb")
    def testdb():
        try:
            count = Product.query.count()
            return f"Database working ✅ | Products: {count}"
        except Exception as e:
            return f"DB ERROR: {e}"

    # ================= HOME =================
    @app.route("/")
    def index():
        try:
            products = Product.query.all()
            print("DEBUG PRODUCTS:", products)
            return render_template("index.html", products=products)
        except Exception as e:
            return f"Error loading products: {e}"

    # ================= LOGIN =================
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
                login_user(user)
                session.permanent = True
                return redirect("/")

            return render_template(
                "login.html",
                error="Invalid username or password"
            )

        return render_template("login.html")

    # ================= LOGOUT =================
    @app.route("/logout")
    @login_required
    def logout():
        logout_user()
        return redirect("/")

    # ================= ADD TO CART =================
    @app.route("/add_to_cart", methods=["POST"])
    @login_required
    def add_to_cart():
        data = request.json
        product_id = data["id"]

        item = Cart.query.filter_by(
            user_id=current_user.id,
            product_id=product_id
        ).first()

        if item:
            item.quantity += 1
        else:
            db.session.add(
                Cart(
                    user_id=current_user.id,
                    product_id=product_id,
                    quantity=1
                )
            )

        db.session.commit()
        return jsonify({"msg": "added"})

    # ================= CART =================
    @app.route("/cart")
    @login_required
    def cart():
        items = Cart.query.filter_by(user_id=current_user.id).all()

        cart_data = []
        total = 0

        for item in items:
            product = Product.query.get(item.product_id)
            subtotal = product.price * item.quantity
            total += subtotal

            cart_data.append({
                "name": product.name,
                "price": product.price,
                "quantity": item.quantity,
                "subtotal": subtotal
            })

        return render_template("cart.html", items=cart_data, total=total)

    # ================= CHECKOUT =================
    @app.route("/checkout", methods=["POST"])
    @login_required
    def checkout():
        cart_items = Cart.query.filter_by(user_id=current_user.id).all()

        if not cart_items:
            return "Cart is empty"

        for item in cart_items:
            product = Product.query.get(item.product_id)

            db.session.add(
                Order(
                    username=current_user.username,
                    product_name=product.name,
                    price=product.price,
                    quantity=item.quantity,
                    total=product.price * item.quantity
                )
            )

        Cart.query.filter_by(user_id=current_user.id).delete()
        db.session.commit()

        return render_template("success.html")

    # ================= ORDERS =================
    @app.route("/orders")
    @login_required
    def orders():
        orders = Order.query.filter_by(
            username=current_user.username
        ).all()

        return render_template("orders.html", orders=orders)

    return app


app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=True)
