from flask import Flask, request, jsonify, redirect, render_template, flash, session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from db import init_db, db
from db_init import create_tables
from models.models import User, Product, Cart, Order
from datetime import timedelta
import os

login_manager = LoginManager()


def create_app():
    app = Flask(__name__)

    # ================= CONFIG =================
    app.config["SECRET_KEY"] = "super-secret-key-change-this"
    app.config["SESSION_COOKIE_SECURE"] = True
    app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
    app.config["SESSION_COOKIE_HTTPONLY"] = True
    app.permanent_session_lifetime = timedelta(days=1)

    # ================= DATABASE =================
    init_db(app)

    with app.app_context():
        create_tables(app)

    # ================= LOGIN MANAGER =================
    login_manager.init_app(app)
    login_manager.login_view = "login"
    login_manager.login_message = None  # 🔥 disable default "Please log in" message

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # ================= HOME =================
    @app.route("/")
    def index():
        products = Product.query.all()
        return render_template("index.html", products=products)

    # ================= LOGIN =================
    @app.route("/login", methods=["POST"])
    def login():

        # 🔥 Clear old flash messages
        session.pop('_flashes', None)

        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username=username).first()

        if not user:
            flash("User not found. Please register.")
            return redirect("/register")

        if user.password != password:
            flash("Incorrect password.")
            return redirect("/")

        login_user(user)

        # 🔥 Clear flashes again after success
        session.pop('_flashes', None)

        return redirect("/")

    # ================= REGISTER =================
    @app.route("/register", methods=["GET", "POST"])
    def register():

        if request.method == "POST":
            session.pop('_flashes', None)

            username = request.form.get("username")
            password = request.form.get("password")

            if User.query.filter_by(username=username).first():
                flash("User already exists.")
                return redirect("/")

            new_user = User(username=username, password=password)
            db.session.add(new_user)
            db.session.commit()

            flash("Registration successful. Please login.")
            return redirect("/")

        return render_template("register.html")

    # ================= LOGOUT =================
    @app.route("/logout")
    @login_required
    def logout():
        logout_user()
        session.pop('_flashes', None)
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
            flash("Cart is empty.")
            return redirect("/")

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

        flash("Order placed successfully!")
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
