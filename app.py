from flask import Flask, request, jsonify, redirect, render_template, flash, session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from db import init_db, db
from db_init import create_tables
from models.models import User, Product, Cart, Order
from config import Config, ADMIN_USERNAME, ADMIN_PASSWORD
import uuid

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

        search = request.args.get("q")

        if search:
            products = Product.query.filter(
                Product.name.ilike(f"%{search}%")
            ).all()
        else:
            products = Product.query.all()

        return render_template("index.html", products=products)

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

        # check exists
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
            new_item = Cart(
                user_id=current_user.id,
                product_id=product_id,
                quantity=1
            )
            db.session.add(new_item)

        db.session.commit()

        return jsonify({"status": "added"})

    # ================= UPDATE CART =================

    @app.route("/update_cart", methods=["POST"])
    @login_required
    def update_cart():

        data = request.json

        product_id = data.get("id")
        action = data.get("action")

        item = Cart.query.filter_by(
            user_id=current_user.id,
            product_id=product_id
        ).first()

        if not item:
            return jsonify({"status": "error"})

        if action == "increase":
            item.quantity += 1

        elif action == "decrease":

            if item.quantity > 1:
                item.quantity -= 1
            else:
                db.session.delete(item)
                db.session.commit()
                return jsonify({"removed": True})

        db.session.commit()

        product = Product.query.get(product_id)

        subtotal = product.price * item.quantity

        total = sum(
            Product.query.get(i.product_id).price * i.quantity
            for i in Cart.query.filter_by(user_id=current_user.id).all()
        )

        return jsonify({
            "quantity": item.quantity,
            "subtotal": subtotal,
            "total": total
        })

    # ================= CART PAGE =================

    @app.route("/cart")
    @login_required
    def cart():

        items = Cart.query.filter_by(user_id=current_user.id).all()

        cart_items = []
        total = 0

        for item in items:

            product = Product.query.get(item.product_id)

            subtotal = product.price * item.quantity

            total += subtotal

            cart_items.append({
                "product_id": product.id,
                "name": product.name,
                "price": product.price,
                "quantity": item.quantity,
                "subtotal": subtotal
            })

        return render_template(
            "cart.html",
            items=cart_items,
            total=total
        )

    # ================= CHECKOUT =================
    @app.route("/checkout")
    @login_required
    def checkout():
    
        cart_items = Cart.query.filter_by(user_id=current_user.id).all()
    
        if not cart_items:
            flash("Cart is empty")
            return redirect("/")
    
        for item in cart_items:
    
            product = Product.query.get(item.product_id)
    
            order = Order(
                order_number=str(uuid.uuid4())[:10].upper(),
    
                username=current_user.username,
                phone=current_user.phone,
                address=current_user.address,
    
                product_name=product.name,
                price=product.price,
                quantity=item.quantity,
                total=product.price * item.quantity,
    
                payment_method="COD",
                payment_status="Pending",
                status="Pending"
            )
    
            db.session.add(order)
    
        # Clear cart
        Cart.query.filter_by(user_id=current_user.id).delete()
        db.session.commit()
    
        flash("Order placed successfully!")
        return redirect("/my_orders")
    
     
    # ================= MY ORDERS =================
    @app.route("/my_orders")
    @login_required
    def my_orders():
    
        orders = Order.query.filter_by(
            username=current_user.username
        ).order_by(Order.created_at.desc()).all()
    
        return render_template("orders.html", orders=orders)

  
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

    # ================= ADMIN LOGIN =================

    @app.route("/admin", methods=["GET", "POST"])
    def admin():

        if request.method == "POST":

            username = request.form.get("username")
            password = request.form.get("password")

            if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:

                session["admin"] = True

                return redirect("/admin/dashboard")

            flash("Invalid admin login")

        return render_template("admin/login.html")

    # ================= ADMIN DASHBOARD =================

    @app.route("/admin/dashboard")
    def admin_dashboard():

        if not session.get("admin"):
            return redirect("/admin")

        products = Product.query.all()

        orders = Order.query.all()

        users = User.query.all()

        return render_template(
            "admin/dashboard.html",
            products=products,
            orders=orders,
            users=users
        )

    # ================= ADMIN LOGOUT =================

    @app.route("/admin/logout")
    def admin_logout():

        session.pop("admin", None)

        return redirect("/admin")

    return app


# ================= RUN =================

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
