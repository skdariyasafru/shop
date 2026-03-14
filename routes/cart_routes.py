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

    cart_count = db.session.query(
        db.func.sum(Cart.quantity)
    ).filter(
        Cart.user_id == current_user.id
    ).scalar() or 0

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

    if action == "increase":
        item.quantity += 1

    elif action == "decrease":

        if item.quantity > 1:
            item.quantity -= 1

        else:
            db.session.delete(item)
            db.session.commit()

            cart_count = db.session.query(
                db.func.sum(Cart.quantity)
            ).filter(
                Cart.user_id == current_user.id
            ).scalar() or 0

            total = db.session.query(
                db.func.sum(Product.price * Cart.quantity)
            ).select_from(Cart).join(
                Product, Cart.product_id == Product.id
            ).filter(
                Cart.user_id == current_user.id
            ).scalar() or 0

            return jsonify({
                "removed": True,
                "total": total,
                "cart_count": cart_count
            })

    db.session.commit()

    subtotal = product.price * item.quantity

    total = db.session.query(
        db.func.sum(Product.price * Cart.quantity)
    ).select_from(Cart).join(
        Product, Cart.product_id == Product.id
    ).filter(
        Cart.user_id == current_user.id
    ).scalar() or 0

    cart_count = db.session.query(
        db.func.sum(Cart.quantity)
    ).filter(
        Cart.user_id == current_user.id
    ).scalar() or 0

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

    items = db.session.query(
        Cart.quantity,
        Product.id,
        Product.name,
        Product.price
    ).select_from(Cart).join(
        Product, Cart.product_id == Product.id
    ).filter(
        Cart.user_id == current_user.id
    ).all()

    cart_items = []
    total = 0

    for quantity, pid, name, price in items:

        subtotal = price * quantity
        total += subtotal

        cart_items.append({
            "product_id": pid,
            "name": name,
            "price": price,
            "quantity": quantity,
            "subtotal": subtotal
        })

    return render_template(
        "cart.html",
        items=cart_items,
        total=total
    )
