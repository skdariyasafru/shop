from datetime import datetime
from flask import Blueprint, redirect, flash, render_template
from flask_login import login_required, current_user

from models.models import Cart, Product, Order
from db import db

order_bp = Blueprint("order", __name__)


@order_bp.route("/checkout")
@login_required
def checkout():

    cart_items = Cart.query.filter_by(
        user_id=current_user.id
    ).all()

    if not cart_items:
        flash("Cart is empty")
        return redirect("/")

    order_number = "ORD-" + datetime.now().strftime(
        "%Y%m%d%H%M%S"
    )

    total_pv = 0

    for item in cart_items:

        product = Product.query.get(
            item.product_id
        )

        if not product:
            continue

        order = Order(
            order_number=order_number,
            username=current_user.username,
            phone=current_user.phone,
            address=current_user.address,
            product_name=product.name,
            price=product.price,
            quantity=item.quantity,
            total=product.price * item.quantity,
            pv_points=product.pv_value * item.quantity,
            status="Pending"
        )

        db.session.add(order)

        # Add PV
        total_pv += (
            product.pv_value * item.quantity
        )

    # Update user PV points
    current_user.points += int(total_pv)

    db.session.add(current_user)

    # Clear cart
    Cart.query.filter_by(
        user_id=current_user.id
    ).delete()

    db.session.commit()

    flash(
        f"Order placed successfully! PV Added: {int(total_pv)}"
    )

    return redirect("/my_orders")


@order_bp.route("/order/<order_number>")
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


@order_bp.route("/my_orders")
@login_required
def my_orders():

    orders = Order.query.filter_by(
        username=current_user.username
    ).order_by(
        Order.created_at.desc()
    ).all()

    return render_template(
        "orders.html",
        orders=orders
    )
