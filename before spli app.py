from flask import Flask, request, jsonify, redirect, render_template
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from db import init_db, db
from db_init import create_tables
from models.models import User, Product, Cart, Order
from datetime import timedelta
import os

login_manager = LoginManager()
login_manager.login_view = "login"


def create_app():
    app = Flask(__name__)

    # Session config (Render friendly)
    app.config["SECRET_KEY"] = "super-secret-key-change-this"
    app.config["SESSION_COOKIE_SECURE"] = True
    app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
    app.permanent_session_lifetime = timedelta(days=1)

    # Database setup
    init_db(app)

    with app.app_context():
        create_tables(app)

    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # ================= HOME =================
    @app.route("/")
    def index():
        products = Product.query.all()
        return render_template("index.html", products=products)

    # ================= LOGIN =================
    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            user = User.query.filter_by(
                username=request.form.get("username"),
                password=request.form.get("password")
            ).first()

            if user:
                login_user(user)
                return redirect("/")

            return "Invalid login"

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
            db.session.add(Cart(
                user_id=current_user.id,
                product_id=product_id,
                quantity=1
            ))

        db.session.commit()
        return jsonify({"msg": "added"})

    # ================= CART PAGE =================
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
            return "Cart is empty!"

        for item in cart_items:
            product = Product.query.get(item.product_id)

            order = Order(
                username=current_user.username,
                product_name=product.name,
                price=product.price,
                quantity=item.quantity,
                total=product.price * item.quantity
            )
            db.session.add(order)

        Cart.query.filter_by(user_id=current_user.id).delete()
        db.session.commit()

        return render_template("success.html")

    # ================= ORDERS =================
    @app.route("/orders")
    @login_required
    def orders():
        user_orders = Order.query.filter_by(
            username=current_user.username
        ).all()

        return render_template("orders.html", orders=user_orders)

    return app


app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
