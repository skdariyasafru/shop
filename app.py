
from flask import Flask, redirect
from flask_login import LoginManager
from config import Config
from db import init_db
from db_init import create_tables
from models.models import User

from routes.auth_routes import auth_bp
from routes.cart_routes import cart_bp
from routes.order_routes import order_bp

login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    init_db(app)

    with app.app_context():
        create_tables(app)

    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message = None

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    @login_manager.unauthorized_handler
    def unauthorized():
        return redirect("/?login=1")

    app.register_blueprint(auth_bp)
    app.register_blueprint(cart_bp)
    app.register_blueprint(order_bp)

    return app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
