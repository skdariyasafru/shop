from flask import Blueprint, request, render_template, jsonify
from models.models import Product

product_bp = Blueprint("product", __name__)


@product_bp.route("/")
def index():
    search = request.args.get("q", "").strip()

    query = Product.query

    if search:
        query = query.filter(Product.name.ilike(f"%{search}%"))

    products = query.order_by(Product.id.desc()).all()

    return render_template("index.html", products=products)

@app.route("/search")
def search():

    q = request.args.get("q", "").strip()

    if q == "":
        products = Product.query.all()
    else:
        products = Product.query.filter(
            Product.name.ilike(f"%{q}%")
        ).all()

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


@product_bp.route("/product/<int:id>")
def product_detail(id):
    product = Product.query.get_or_404(id)
    return render_template("product_detail.html", product=product)
