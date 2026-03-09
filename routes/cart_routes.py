from flask import Blueprint, jsonify, request, render_template
from flask_login import login_required, current_user
from db import db
from models.models import Cart, Product

cart_bp = Blueprint("cart", __name__)


# ================= ADD TO CART =================

@cart_bp.route("/add_to_cart", methods=["POST"])
def add_to_cart():

    if not current_user.is_authenticated:
        return jsonify({"status": "login_required"}), 401

    pid = request.json.get("id")

    item = Cart.query.filter_by(
        user_id=current_user.id,
        product_id=pid
    ).first()

    if item:
        item.quantity += 1
    else:
        item = Cart(
            user_id=current_user.id,
            product_id=pid,
            quantity=1
        )
        db.session.add(item)

    db.session.commit()

    return jsonify({
        "status": "added",
        "quantity": item.quantity
    })


# ================= UPDATE CART =================

@cart_bp.route("/update_cart", methods=["POST"])
def update_cart():

    if not current_user.is_authenticated:
        return jsonify({"status": "login_required"}), 401

    pid = request.json.get("id")
    action = request.json.get("action")

    item = Cart.query.filter_by(
        user_id=current_user.id,
        product_id=pid
    ).first()

    if not item:
        return jsonify({"error": "Item not found"}), 404

    product = Product.query.get(pid)

    # Increase quantity
    if action == "increase":
        item.quantity += 1

    # Decrease quantity
    elif action == "decrease":
        item.quantity -= 1

    # Remove item if quantity becomes 0
    if item.quantity <= 0:
        db.session.delete(item)
        db.session.commit()

        # calculate total
        items = Cart.query.filter_by(user_id=current_user.id).all()
        total = sum(Product.query.get(i.product_id).price * i.quantity for i in items)

        return jsonify({
            "removed": True,
            "total": total
        })

    db.session.commit()

    subtotal = product.price * item.quantity

    # calculate total
    items = Cart.query.filter_by(user_id=current_user.id).all()
    total = sum(Product.query.get(i.product_id).price * i.quantity for i in items)

    return jsonify({
        "quantity": item.quantity,
        "subtotal": subtotal,
        "total": total
    })


# ================= CART PAGE =================

@cart_bp.route("/cart")
@login_required
def cart():

    cart_items = Cart.query.filter_by(user_id=current_user.id).all()

    items = []
    total = 0

    for i in cart_items:

        product = Product.query.get(i.product_id)

        subtotal = product.price * i.quantity
        total += subtotal

        items.append({
            "id": product.id,
            "name": product.name,
            "price": product.price,
            "quantity": i.quantity,
            "subtotal": subtotal
        })

    return render_template(
        "cart.html",
        items=items,
        total=total
    )
