plase update my search 
from flask import Blueprint, request, render_template, jsonify
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
        query = query.filter(Product.name.ilike(f"%{search}%"))

    products = query.order_by(Product.id.desc()).all()

    return render_template("index.html", products=products)


# =========================
# AJAX SEARCH API
# =========================
@product_bp.route("/search")
def search():

    q = request.args.get("q", "").strip()

    if q:
        products = Product.query.filter(
            Product.name.ilike(f"%{q}%")
        ).all()
    else:
        products = Product.query.order_by(Product.id.desc()).all()

    data = []

    for p in products:
        data.append({
            "id": p.id,
            "name": p.name,
            "price": p.price,
            "image": p.image
        })

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
    )    amazon style and 10x faster 
