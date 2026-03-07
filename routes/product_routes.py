from flask import Blueprint, request, render_template, jsonify
from sqlalchemy import or_
from models.models import Product

product_bp = Blueprint("product", __name__)


# =========================
# HOME PAGE
# =========================
@product_bp.route("/")
def index():

    search = request.args.get("q", "").strip()

    query = Product.query

    if search:
        query = query.filter(
            or_(
                Product.name.ilike(f"%{search}%"),
                Product.description.ilike(f"%{search}%"),
                Product.category.ilike(f"%{search}%")
            )
        )

    products = query.order_by(Product.id.desc()).limit(50).all()

    return render_template("index.html", products=products)


# =========================
# FAST AJAX SEARCH API
# =========================
@product_bp.route("/search")
def search():

    q = request.args.get("q", "").strip()

    query = Product.query

    if q:
        query = query.filter(
            or_(
                Product.name.ilike(f"%{q}%"),
                Product.description.ilike(f"%{q}%"),
                Product.category.ilike(f"%{q}%")
            )
        )

    # limit results for speed
    products = query.order_by(Product.id.desc()).limit(20).all()

    data = [
        {
            "id": p.id,
            "name": p.name,
            "price": p.price,
            "image": p.image
        }
        for p in products
    ]

    return jsonify(data)


# =========================
# PRODUCT DETAIL PAGE
# =========================
@product_bp.route("/product/<int:id>")
def product_detail(id):

    product = Product.query.get_or_404(id)

    return render_template(
        "product_detail.html",
        product=product
    )
