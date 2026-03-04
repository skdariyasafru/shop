# ==========================================================
# IMPORTS
# ==========================================================
from flask_login import login_required, current_user
from models.models import Cart, Product
from db import db
from flask import Blueprint, request, jsonify, render_template



# ==========================================================
# BLUEPRINT CONFIGURATION
# ==========================================================
cart_bp = Blueprint("cart", __name__, url_prefix="")


# ==========================================================
# ADD PRODUCT TO CART
# ==========================================================
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

    return jsonify({
        "status": "added",
        "quantity": item.quantity
    })


# ==========================================================
# UPDATE CART (INCREASE / DECREASE QUANTITY)
# ==========================================================
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

    if action == "increase":
        item.quantity += 1

    elif action == "decrease":
        if item.quantity > 1:
            item.quantity -= 1
        else:
            db.session.delete(item)
            db.session.commit()

            return jsonify({
                "removed": True
            })

    db.session.commit()

    product = Product.query.get(product_id)
    subtotal = product.price * item.quantity

    # calculate total cart price
    items = db.session.query(Cart, Product).join(
        Product, Cart.product_id == Product.id
    ).filter(
        Cart.user_id == current_user.id
    ).all()

    total = sum(p.price * c.quantity for c, p in items)

    return jsonify({
        "quantity": item.quantity,
        "subtotal": subtotal,
        "total": total
    })


# ==========================================================
# DISPLAY CART PAGE
# ==========================================================
@cart_bp.route("/cart")
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

    return render_template(
        "cart.html",
        items=cart_items,
        total=total
    )
