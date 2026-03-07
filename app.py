import os
from flask import Flask
from flask_login import LoginManager
from config import Config
from db import init_db
from models.models import User

# blueprints
from routes.auth_routes import auth_bp
from routes.product_routes import product_bp
from routes.cart_routes import cart_bp
from routes.order_routes import order_bp
from routes.profile_routes import profile_bp


login_manager = LoginManager()


def create_app():

    app = Flask(__name__)
    app.config.from_object(Config)

    # initialize database safely
    with app.app_context():
        init_db(app)

    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message = None

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # register blueprints
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
