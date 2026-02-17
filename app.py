
import os
from flask import Flask, render_template, request, redirect, session, flash
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    price = db.Column(db.Float)
    image = db.Column(db.String(500))

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    product_name = db.Column(db.String(200))
    price = db.Column(db.Float)
    quantity = db.Column(db.Integer)
    total = db.Column(db.Float)

def create_app():
    app = Flask(__name__)

    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "secret123")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
    ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            if request.form.get("username") == ADMIN_USERNAME and request.form.get("password") == ADMIN_PASSWORD:
                session["admin"] = True
                return redirect("/admin/dashboard")
            flash("Invalid login")
        return render_template("admin/login.html")

    @app.route("/logout")
    def logout():
        session.clear()
        return redirect("/login")

    @app.route("/admin/dashboard")
    def dashboard():
        if not session.get("admin"):
            return redirect("/login")
        return render_template("admin/dashboard.html",
            product_count=Product.query.count(),
            order_count=Order.query.count()
        )

    @app.route("/admin/products")
    def products():
        if not session.get("admin"):
            return redirect("/login")
        return render_template("admin/products.html", products=Product.query.all())

    @app.route("/admin/add_product", methods=["GET","POST"])
    def add_product():
        if not session.get("admin"):
            return redirect("/login")
        if request.method == "POST":
            p = Product(
                name=request.form.get("name"),
                price=request.form.get("price"),
                image=request.form.get("image")
            )
            db.session.add(p)
            db.session.commit()
            return redirect("/admin/products")
        return render_template("admin/add_product.html")

    @app.route("/admin/delete_product/<int:id>")
    def delete_product(id):
        if not session.get("admin"):
            return redirect("/login")
        db.session.delete(Product.query.get(id))
        db.session.commit()
        return redirect("/admin/products")

    @app.route("/admin/orders")
    def orders():
        if not session.get("admin"):
            return redirect("/login")
        return render_template("admin/orders.html", orders=Order.query.all())

    return app

app = create_app()

if __name__ == "__main__":
    app.run()
