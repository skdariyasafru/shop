import os
import threading
import time
import requests

from flask import Flask
from flask_login import LoginManager

from config import Config
from db import init_db, db
from models.models import User


login_manager = LoginManager()


def self_ping():

    url = "https://shop-1-tvqs.onrender.com/ping"

    while True:
        try:
            requests.get(url, timeout=10)
        except Exception:
            pass

        time.sleep(300)


def create_app():

    app = Flask(__name__)
    app.config.from_object(Config)

    init_db(app)

    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message = None

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    @app.route("/ping")
    def ping():
        return "alive"

    if os.environ.get("RENDER"):
        threading.Thread(target=self_ping, daemon=True).start()

    from routes.auth_routes import auth_bp
    from routes.product_routes import product_bp
    from routes.cart_routes import cart_bp
    from routes.order_routes import order_bp
    from routes.profile_routes import profile_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(product_bp)
    app.register_blueprint(cart_bp)
    app.register_blueprint(order_bp)
    app.register_blueprint(profile_bp)

    return app


app = create_app()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
