import os
import uuid
from datetime import datetime

from flask import Flask, request, jsonify, redirect, render_template, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

from db import init_db, db
from models.models import User, Product, Cart, Order
from config import Config


login_manager = LoginManager()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # ================= DATABASE INIT =================
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
        return jsonify({"error": "Unauthorized"}), 401


    # =================================================
    # HOME
    # =================================================
    @app.route("/")
    def index():
        products = Product.query.order_by(Product.id.desc()).all()
        return render_template("index.html", products=products)


    # =================================================
    # SEARCH (AUTO LOAD + SINGLE LETTER SUPPORT)
    # =================================================
    @app.route("/search")
    def search():
        query = request.args.get("q", "").strip()

        if query == "":
            products = Product.query.order_by(Product.id.desc()).all()
        else:
            products = Product.query.filter(
                Product.name.ilike(f"%{query}%")
            ).order_by(Product.id.desc()).all()

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

        if User.query.filter_by(username=username).first():
            flash("User already exists")
            return redirect("/?login=1")

        new_user = User(
            username=username,
            password=password,
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
        return redirect("/")


    # =================================================
    # ADD TO CART
    # =================================================
    @app.route("/add_to_cart", methods=["POST"])
    @login_required
    def add_to_cart():

        data = request.get_json()
        product_id = data.get("id")

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
    # UPDATE CART (FULLY DYNAMIC)
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

                total = calculate_cart_total()
                return jsonify({
                    "removed": True,
                    "total": total
                })

        db.session.commit()

        product = Product.query.get(product_id)
        subtotal = product.price * item.quantity
        total = calculate_cart_total()

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
    # HELPER FUNCTION
    # =================================================
    def calculate_cart_total():
        items = db.session.query(Cart, Product).join(
            Product, Cart.product_id == Product.id
        ).filter(
            Cart.user_id == current_user.id
        ).all()

        return sum(p.price * c.quantity for c, p in items)


    return app


# IMPORTANT FOR RENDER
app = create_app()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
