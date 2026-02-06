from flask import Flask
from flask_login import LoginManager
from db import init_db
from db_init import create_tables
import os
from models import User, Product, Cart, Order

login_manager = LoginManager()
login_manager.login_view = "auth.login"

def create_app():
    app = Flask(__name__)

    app.config["SECRET_KEY"] = "secret"

    init_db(app)
    create_tables(app)

    login_manager.init_app(app)

    from models.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from routes.auth import auth_bp
    app.register_blueprint(auth_bp)

    return app
@app.route("/add_to_cart", methods=["POST"])
def add_to_cart():
    if "user" not in session:
        return redirect("/login")

    data = request.json

    item = Cart(
        user=session["user"],
        product_name=data["name"],
        price=data["price"]
    )

    db.session.add(item)
    db.session.commit()

    return jsonify({"msg": "added"})
@app.route("/cart")
def view_cart():
    if "user" not in session:
        return redirect("/login")

    items = Cart.query.filter_by(user=session["user"]).all()
    total = sum(i.price for i in items)

    return render_template("cart.html", items=items, total=total)
@app.route("/checkout")
def checkout():
    if "user" not in session:
        return redirect("/login")

    items = Cart.query.filter_by(user=session["user"]).all()

    for i in items:
        order = Order(
            user=i.user,
            product_name=i.product_name,
            price=i.price
        )
        db.session.add(order)
        db.session.delete(i)

    db.session.commit()

    return redirect("/")

app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
