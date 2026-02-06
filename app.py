from flask import Flask
from flask_login import LoginManager
from db import init_db
from db_init import create_tables
import os

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

app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
