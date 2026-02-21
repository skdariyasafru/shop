from flask import Flask, request, jsonify, redirect, render_template, flash, session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from db import init_db, db
from db_init import create_tables
from models.models import User, Product, Cart, Order
from config import Config
import uuid
from datetime import datetime

login_manager = LoginManager()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # ================= INIT DATABASE =================
    init_db(app)

    with app.app_context():
        create_tables(app)

    # ================= LOGIN MANAGER =================
    login_manager.init_app(app)
    login_manager.login_view = "login"
    login_manager.login_message = None

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    @login_manager.unauthorized_handler
    def unauthorized():
        return redirect("/?login=1")

    # ================= HOME =================
    @app.route("/")
    def index():
        try:
            search = request.args.get("q")

            if search:
                products = Product.query.filter(
                    Product.name.ilike(f"%{search}%")
                ).all()
            else:
                products = Product.query.all()

            return render_template("index.html", products=products)

        except Exception as e:
            return f"Home Error: {str(e)}"

    # ================= SEARCH API =================
    @app.route("/search")
    def search():
        try:
            query = request.args.get("q", "")

            if not query:
                return jsonify([])

            products = Product.query.filter(
                Product.name.ilike(f"%{query}%")
            ).limit(10).all()

            result = [
                {
                    "id": p.id,
                    "name": p.name,
                    "price": p.price,
                    "image": p.image
                }
                for p in products
            ]

            return jsonify(result)

        except Exception as e:
            print("Search error:", e)
            return jsonify([])

    # ================= PRODUCT DETAIL =================
    @app.route("/product/<int:id>")
    def product_detail(id):
        try:
            product = Product.query.filter_by(id=id).first()

            if not product:
                return "Product not found", 404

            return render_template("product_detail.html", product=product)

        except Exception as e:
            return f"Product Error: {str(e)}"

    # ================= LOGIN =================
    @app.route("/login", methods=["POST"])
    def login():
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username=username).first()

        if not user:
            flash("User not found")
            return redirect("/?login=1")

        if user.password != password:
            flash("Incorrect password")
            return redirect("/?login=1")

        login_user(user)
        flash("Login successful")
        return redirect("/")

    # ================= REGISTER =================
    @app.route("/register", methods=["POST"])
    def register():
        username = request.form.get("username")
        password = request.form.get("password")
        phone = request.form.get("phone")
        address = request.form.get("address")
        referral = request.form.get("referral")

        if User.query.filter_by(username=username).first():
            flash("User already exists")
            return redirect("/?login=1")

        referral_code = str(uuid.uuid4())[:8]

        user = User(
            username=username,
            password=password,
            phone=phone,
            address=address,
            referral_code=referral_code,
            referred_by=referral,
            points=0
        )

        db.session.add(user)
        db.session.commit()

        flash("Registration successful")
        return redirect("/?login=1")

    # ================= LOGOUT =================
    @app.route("/logout")
    @login_required
    def logout():
        logout_user()
        flash("Logged out")
        return redirect("/")

    # ================= ADD TO CART =================
    @app.route("/add_to_cart", methods=["POST"])
    @login_required
    def add_to_cart():
        product_id = request.json.get("id")

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
        return jsonify({"status": "added"})

    # ================= CART PAGE =================
    @app.route("/cart")
    @login_required
    def cart():
        items = Cart.query.filter_by(user_id=current_user.id).all()

        cart_items = []
        total = 0

        for item in items:
            product = Product.query.filter_by(id=item.product_id).first()
            if not product:
                continue

            subtotal = product.price * item.quantity
            total += subtotal

            cart_items.append({
                "product_id": product.id,
                "name": product.name,
                "price": product.price,
                "quantity": item.quantity,
                "subtotal": subtotal
            })

        return render_template("cart.html", items=cart_items, total=total)

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
