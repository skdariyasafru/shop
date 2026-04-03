/* ================= CART FUNCTIONS ================= */

window.addToCart = function(productId) {

    fetch("/add_to_cart", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ id: productId })
    })
    .then(res => {

        if (res.status === 401) {
            if (typeof openLogin === "function") {
                openLogin();
            }
            return null;
        }

        return res.json();
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

    if action == "increase":
        item.quantity += 1

    elif action == "decrease":

        if item.quantity > 1:
            item.quantity -= 1
        else:
            db.session.delete(item)
            db.session.commit()

/* ================= CHANGE QTY ================= */

window.changeQty = function(productId, action) {

    fetch("/update_cart", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            id: productId,
            action: action
        })
    })
    .then(res => {

        if (res.status === 401) {
            if (typeof openLogin === "function") {
                openLogin();
            }
            return null;
        }

        return res.json();
    })
    .then(data => {

            total = result[0] or 0
            cart_count = result[1] or 0

            return jsonify({
                "removed": True,
                "total": total,
                "cart_count": cart_count
            })

    db.session.commit()

    product = db.session.get(Product, product_id)

    subtotal = product.price * item.quantity

    result = db.session.query(
        db.func.sum(Product.price * Cart.quantity),
        db.func.sum(Cart.quantity)
    ).select_from(Cart).join(
        Product, Cart.product_id == Product.id
    ).filter(
        Cart.user_id == current_user.id
    ).first()

    total = result[0] or 0
    cart_count = result[1] or 0

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

    el.innerText = count ?? 0;
}
