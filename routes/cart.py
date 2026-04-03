from flask import Blueprint, render_template
from flask_login import current_user, login_required

cart_bp = Blueprint("cart", __name__)


@cart_bp.route("/cart")
@login_required
def cart():

    # Get cart items from user
    cart_items = current_user.cart if hasattr(current_user, "cart") else []

    items = []
    total = 0

    for item in cart_items:
        subtotal = item.price * item.quantity
        total += subtotal

        items.append({
            "product_id": item.product_id,
            "name": item.product.name if hasattr(item, "product") else "Product",
            "price": item.price,
            "quantity": item.quantity,
            "subtotal": subtotal
        })

    return render_template("cart.html", items=items, total=total)
