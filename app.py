from flask import Flask
from flask_login import LoginManager
#from config import Config
from db import db, init_db
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://dariya:iXXzwPV9FQzQLqEUw35PJq9f3ItUT4rX@dpg-d5j4o50gjchc73cu2hsg-a/shop_aizq"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.login_view = "auth.login"


def create_app():
    app = Flask(__name__)
    
    # Load config
    app.config["SECRET_KEY"] = "secret"

    # Initialize PostgreSQL database
    init_db(app)

    # Initialize login manager
    login_manager.init_app(app)

    # Import models AFTER db init
    from models.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register routes
    from routes.auth import auth_bp
    app.register_blueprint(auth_bp)

    return app


app = create_app()

if __name__ == "__main__":
    app.run()
