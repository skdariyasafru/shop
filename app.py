import os
import time

from flask import Flask, jsonify, request
from flask_login import LoginManager, current_user

from config import Config
from db import init_db, db
from models.models import User


login_manager = LoginManager()


def create_app():

    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize database
    init_db(app)

    # ================= LOGIN MANAGER =================
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message = None

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))


    # ================= REQUEST TIMER =================
    @app.before_request
    def start_timer():
        try:
            request.start_time = time.time()
        except Exception:
            request.start_time = None

    @app.after_request
    def log_time(response):
        try:
            if hasattr(request, "start_time") and request.start_time:
                duration = time.time() - request.start_time
                print(f"{request.path} took {duration:.2f}s")
        except Exception:
            pass

        return response


    # ================= LOGIN CHECK =================
    @app.route("/check_login")
    def check_login():
        return jsonify({
            "logged_in": current_user.is_authenticated
        })


    # ================= BLUEPRINTS =================
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


# ================= RUN APP =================
app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)



