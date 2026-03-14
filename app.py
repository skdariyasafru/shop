import os
import threading
import time
import requests

from flask import Flask
from flask_login import LoginManager

from config import Config
from db import init_db
from models.models import User


# ================= LOGIN MANAGER =================
login_manager = LoginManager()


# ================= SELF PING FUNCTION =================
def self_ping():

    url = "https://shop-1-tvqs.onrender.com/ping"

    while True:
        try:
            requests.get(url, timeout=10)
        except Exception:
            pass

        # wait 5 minutes
        time.sleep(280)

# ================= CREATE APP =================
def create_app():

    app = Flask(__name__)
    app.config.from_object(Config)

    # initialize database
    init_db(app)

    # login manager setup
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message = None

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # lightweight ping route
    @app.route("/ping")
    def ping():
        return "alive"

    # start self ping thread
    threading.Thread(target=self_ping, daemon=True).start()

    # import routes lazily
    from routes.auth_routes import auth_bp
    from routes.product_routes import product_bp
    from routes.cart_routes import cart_bp
    from routes.order_routes import order_bp
    from routes.profile_routes import profile_bp

    # register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(product_bp)
    app.register_blueprint(cart_bp)
    app.register_blueprint(order_bp)
    app.register_blueprint(profile_bp)

    return app


# ================= RUN APP =================
app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
