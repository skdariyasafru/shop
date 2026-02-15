
from flask import Blueprint, redirect, flash, render_template
from flask_login import login_required, current_user
from db import db
from models.models import Cart, Product, Order

order_bp = Blueprint("order", __name__)

@order_bp.route("/checkout")
@login_required
def checkout():
    items = Cart.query.filter_by(user_id=current_user.id).all()
    if not items:
        flash("Cart empty")
        return redirect("/")
    for i in items:
        p = Product.query.get(i.product_id)
        db.session.add(Order(username=current_user.username, product_name=p.name, price=p.price, quantity=i.quantity, total=p.price*i.quantity))
    Cart.query.filter_by(user_id=current_user.id).delete()
    db.session.commit()
    flash("Order placed")
    return redirect("/")

@order_bp.route("/my_orders")
@login_required
def my_orders():
    orders = Order.query.filter_by(username=current_user.username).all()
    return render_template("orders.html", orders=orders)
