
from flask import Blueprint, jsonify, request, render_template
from flask_login import login_required, current_user
from db import db
from models.models import Cart, Product

cart_bp = Blueprint("cart", __name__)

@cart_bp.route("/add_to_cart", methods=["POST"])
def add_to_cart():
    if not current_user.is_authenticated:
        return jsonify({"status":"login_required"}), 401
    pid = request.json.get("id")
    item = Cart.query.filter_by(user_id=current_user.id, product_id=pid).first()
    if item:
        item.quantity += 1
    else:
        db.session.add(Cart(user_id=current_user.id, product_id=pid, quantity=1))
    db.session.commit()
    return jsonify({"status":"added"})

@cart_bp.route("/cart")
@login_required
def cart():
    items = Cart.query.filter_by(user_id=current_user.id).all()
    data = []
    total = 0
    for i in items:
        p = Product.query.get(i.product_id)
        subtotal = p.price * i.quantity
        total += subtotal
        data.append({"name":p.name,"price":p.price,"quantity":i.quantity,"subtotal":subtotal})
    return render_template("cart.html", items=data, total=total)
