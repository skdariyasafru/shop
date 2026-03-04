from datetime import datetime
from flask import Blueprint, redirect, flash, render_template
from flask_login import login_required, current_user
from models.models import Cart, Product, Order
from db import db

order_bp = Blueprint("order", __name__)


@order_bp.route("/checkout")
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


@order_bp.route("/my_orders")
@login_required
def my_orders():

    orders = Order.query.filter_by(
        username=current_user.username
    ).order_by(Order.created_at.desc()).all()

    return render_template("orders.html", orders=orders)