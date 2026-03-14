from flask_login import login_required, current_user
from models.models import Cart, Product
from db import db
from flask import Blueprint, request, jsonify, render_template


# ==========================================================
# BLUEPRINT
# ==========================================================
cart_bp = Blueprint("cart", __name__)


# ================= ADD TO CART =================
@cart_bp.route("/add_to_cart", methods=["POST"])
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

    cart_items = Cart.query.filter_by(user_id=current_user.id).all()
    cart_count = sum(i.quantity for i in cart_items)

    return jsonify({
        "status": "added",
        "quantity": item.quantity,
        "cart_count": cart_count
    })


# ================= UPDATE CART =================
@cart_bp.route("/update_cart", methods=["POST"])
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

    product = Product.query.get(product_id)

    # increase quantity
    if action == "increase":
        item.quantity += 1

    # decrease quantity
    elif action == "decrease":

        if item.quantity > 1:
            item.quantity -= 1

        else:
            db.session.delete(item)
            db.session.commit()

            cart_items = Cart.query.filter_by(user_id=current_user.id).all()

            total = 0
            cart_count = 0

            for c in cart_items:
                p = Product.query.get(c.product_id)
                total += p.price * c.quantity
                cart_count += c.quantity

            return jsonify({
                "removed": True,
                "total": total,
                "cart_count": cart_count
            })

    db.session.commit()

    subtotal = product.price * item.quantity

    cart_items = Cart.query.filter_by(user_id=current_user.id).all()

    total = 0
    cart_count = 0

    for c in cart_items:
        p = Product.query.get(c.product_id)
        total += p.price * c.quantity
        cart_count += c.quantity

    return jsonify({
        "quantity": item.quantity,
        "subtotal": subtotal,
        "total": total,
        "cart_count": cart_count
    })


# ================= CART PAGE =================
@cart_bp.route("/cart")
@login_required
def cart():

    cart_rows = Cart.query.filter_by(user_id=current_user.id).all()

    cart_items = []
    total = 0

    for row in cart_rows:

        product = Product.query.get(row.product_id)

        subtotal = product.price * row.quantity
        total += subtotal

        cart_items.append({
            "product_id": product.id,
            "name": product.name,
            "price": product.price,
            "quantity": row.quantity,
            "subtotal": subtotal
        })

    return render_template(
        "cart.html",
        items=cart_items,
        total=total
    )
