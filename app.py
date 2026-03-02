import os
import uuid
from datetime import datetime

from flask import Flask, request, jsonify, redirect, render_template, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from sqlalchemy import func

from db import init_db, db
from models.models import User, Product, Cart, Order
from config import Config


login_manager = LoginManager()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # ================= DATABASE =================
    init_db(app)

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

    # =================================================
    # HOME
    # =================================================
    @app.route("/")
    def index():
        search = request.args.get("q", "").strip()

        query = Product.query

        if search:
            query = query.filter(Product.name.ilike(f"%{search}%"))

        products = query.order_by(Product.id.desc()).all()

        return render_template("index.html", products=products)

    # =================================================
    # LIVE SEARCH
    # =================================================
    @app.route("/search")
    def search():
        query = request.args.get("q", "").strip()

        if not query:
            return jsonify([])

        products = Product.query.filter(
            Product.name.ilike(f"%{query}%")
        ).limit(10).all()

        return jsonify([
            {
                "id": p.id,
                "name": p.name,
                "price": p.price,
                "image": p.image
            }
            for p in products
        ])

    # =================================================
    # PRODUCT DETAIL
    # =================================================
    @app.route("/product/<int:id>")
    def product_detail(id):
        product = Product.query.get_or_404(id)
        return render_template("product_detail.html", product=product)

    # =================================================
    # LOGIN
    # =================================================
    @app.route("/login", methods=["POST"])
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

    # =================================================
    # REGISTER
    # =================================================
    @app.route("/register", methods=["POST"])
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

    # =================================================
    # LOGOUT
    # =================================================
    @app.route("/logout")
    @login_required
    def logout():
        logout_user()
        flash("Logged out")
        return redirect("/")

    # =================================================
    # ADD TO CART
    # =================================================
    @app.route("/add_to_cart", methods=["POST"])
    @login_required
    def add_to_cart():
        product_id = request.json.get("id")

        product = Product.query.get(product_id)
        if not product:
            return jsonify({"error": "Product not found"}), 404

        item = Cart.query.filter_by(
            user_id=current_user.id,
            product_id=product_id
        ).first()

        if item:
            item.quantity += 1
        else:
            item = Cart(
                user_id=current_user.id,
                product_id=product_id,
                quantity=1
            )
            db.session.add(item)

        db.session.commit()

        return jsonify({
            "status": "added",
            "quantity": item.quantity
        })

    # =================================================
    # UPDATE CART (+ / -)
    # =================================================
    @app.route("/update_cart", methods=["POST"])
    @login_required
    def update_cart():

        data = request.get_json()
        product_id = data.get("id")
        action = data.get("action")

        item = Cart.query.filter_by(
            user_id=current_user.id,
            product_id=product_id
        ).first()

        if not item:
            return jsonify({"error": "Item not found"}), 404

        if action == "increase":
            item.quantity += 1

        elif action == "decrease":
            if item.quantity > 1:
                item.quantity -= 1
            else:
                db.session.delete(item)
                db.session.commit()

                total = db.session.query(
                    func.sum(Product.price * Cart.quantity)
                ).join(Product).filter(
                    Cart.user_id == current_user.id
                ).scalar() or 0

                return jsonify({
                    "removed": True,
                    "total": total
                })

        db.session.commit()

        product = Product.query.get(product_id)
        subtotal = product.price * item.quantity

        total = db.session.query(
            func.sum(Product.price * Cart.quantity)
        ).join(Product).filter(
            Cart.user_id == current_user.id
        ).scalar() or 0

        return jsonify({
            "quantity": item.quantity,
            "subtotal": subtotal,
            "total": total
        })

    # =================================================
    # CART PAGE
    # =================================================
    @app.route("/cart")
    @login_required
    def cart():

        items = db.session.query(Cart, Product).join(
            Product, Cart.product_id == Product.id
        ).filter(
            Cart.user_id == current_user.id
        ).all()

        cart_items = []
        total = 0

        for cart_item, product in items:
            subtotal = product.price * cart_item.quantity
            total += subtotal

            cart_items.append({
                "product_id": product.id,
                "name": product.name,
                "price": product.price,
                "quantity": cart_item.quantity,
                "subtotal": subtotal
            })

        return render_template("cart.html", items=cart_items, total=total)

    # =================================================
    # CHECKOUT
    # =================================================
    @app.route("/checkout")
    @login_required
    def checkout():

        cart_items = Cart.query.filter_by(user_id=current_user.id).all()

        if not cart_items:
            flash("Cart is empty")
            return redirect("/")

        order_number = "ORD-" + datetime.now().strftime("%Y%m%d%H%M%S")

        for item in cart_items:
            product = Product.query.get(item.product_id)

            order = Order(
                order_number=order_number,
                username=current_user.username,
                phone=current_user.phone,
                address=current_user.address,
                product_name=product.name,
                price=product.price,
                quantity=item.quantity,
                total=product.price * item.quantity,
                status="Pending"
            )

            db.session.add(order)

        Cart.query.filter_by(user_id=current_user.id).delete()
        db.session.commit()

        flash("Order placed successfully!")
        return redirect("/my_orders")

    # =================================================
    # MY ORDERS
    # =================================================
    @app.route("/my_orders")
    @login_required
    def my_orders():
        orders = Order.query.filter_by(
            username=current_user.username
        ).order_by(Order.created_at.desc()).all()

        return render_template("orders.html", orders=orders)

    # =================================================
    # ORDER DETAILS
    # =================================================
    @app.route("/order/<order_number>")
    @login_required
    def order_details(order_number):

        orders = Order.query.filter_by(
            order_number=order_number,
            username=current_user.username
        ).all()

        if not orders:
            flash("Order not found")
            return redirect("/my_orders")

        return render_template(
            "order_details.html",
            orders=orders,
            order_number=order_number
        )

    # =================================================
    # PROFILE
    # =================================================
    @app.route("/profile")
    @login_required
    def profile():
        return render_template("profile.html", user=current_user)

    return app


app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
