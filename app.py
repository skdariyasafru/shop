
from flask import Flask, request, redirect, render_template, flash, session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from db import init_db, db
from db_init import create_tables
from models.models import User, Product, Cart, Order
from config import ADMIN_USERNAME, ADMIN_PASSWORD
import uuid

login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    init_db(app)
    create_tables(app)

    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    @app.route("/")
    def index():
        products = Product.query.all()
        return render_template("index.html", products=products)

    @app.route("/login", methods=["POST"])
    def login():
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username=username).first()

        if user and user.password == password:
            login_user(user)
            return redirect("/")

        flash("Invalid login")
        return redirect("/")

    @app.route("/register", methods=["POST"])
    def register():
        username = request.form.get("username")
        password = request.form.get("password")
        phone = request.form.get("phone")
        address = request.form.get("address")
        referral = request.form.get("referral")

        ref_code = str(uuid.uuid4())[:8]

        user = User(
            username=username,
            password=password,
            phone=phone,
            address=address,
            referral_code=ref_code,
            referred_by=referral
        )

        db.session.add(user)
        db.session.commit()

        flash("Registered successfully")
        return redirect("/")

    @app.route("/checkout")
    @login_required
    def checkout():
        cart = Cart.query.filter_by(user_id=current_user.id).all()

        for item in cart:
            product = Product.query.get(item.product_id)

            order = Order(
                username=current_user.username,
                phone=current_user.phone,
                address=current_user.address,
                product_name=product.name,
                price=product.price,
                quantity=item.quantity,
                total=product.price * item.quantity
            )

            db.session.add(order)

        Cart.query.filter_by(user_id=current_user.id).delete()
        db.session.commit()

        flash("Order placed")
        return redirect("/")

    @app.route("/my_orders")
    @login_required
    def my_orders():
        orders = Order.query.filter_by(username=current_user.username).all()
        return render_template("orders.html", orders=orders)

    @app.route("/admin", methods=["GET","POST"])
    def admin_login():
        if request.method == "POST":
            username = request.form.get("username")
            password = request.form.get("password")

            if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
                session["admin"] = True
                return redirect("/admin/dashboard")

            flash("Invalid admin login")

        return render_template("admin/login.html")

    @app.route("/admin/dashboard")
    def admin_dashboard():
        if not session.get("admin"):
            return redirect("/admin")

        products = Product.query.all()
        orders = Order.query.all()

        return render_template("admin/dashboard.html", products=products, orders=orders)

    return app

app = create_app()

if __name__ == "__main__":
    app.run()
