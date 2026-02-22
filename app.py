from flask import Flask, request, jsonify, redirect, render_template, flash, session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from db import init_db, db
from models.models import User, Product, Cart, Order
from config import Config
from datetime import datetime
import uuid

login_manager = LoginManager()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Init DB (NO create_all in production)
    init_db(app)

    login_manager.init_app(app)
    login_manager.login_view = "login"
    login_manager.login_message = None

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    @login_manager.unauthorized_handler
    def unauthorized():
        return redirect("/?login=1")

    # ================= HOME (PAGINATED) =================
    @app.route("/")
    def index():
        page = request.args.get("page", 1, type=int)
        per_page = 20

        search = request.args.get("q", "")

        query = Product.query

        if search:
            query = query.filter(Product.name.ilike(f"{search}%"))

        products = query.paginate(page=page, per_page=per_page, error_out=False)

        return render_template(
            "index.html",
            products=products.items,
            pagination=products
        )

    # ================= SEARCH (OPTIMIZED) =================
    @app.route("/search")
    def search():
        query = request.args.get("q", "")

        if not query or len(query) < 2:
            return jsonify([])

        products = Product.query.filter(
            Product.name.ilike(f"{query}%")
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

    # ================= PRODUCT DETAIL =================
    @app.route("/product/<int:id>")
    def product_detail(id):
        product = Product.query.get_or_404(id)
        return render_template("product_detail.html", product=product)

    # ================= LOGIN =================
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

    # ================= REGISTER =================
    @app.route("/register", methods=["POST"])
    def register():
        username = request.form.get("username")
        password = request.form.get("password")

        if User.query.filter_by(username=username).first():
            flash("User already exists")
            return redirect("/?login=1")

        user = User(
            username=username,
            password=password,
            referral_code=str(uuid.uuid4())[:8],
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

    # ================= CART (JOIN OPTIMIZED) =================
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

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=False)
