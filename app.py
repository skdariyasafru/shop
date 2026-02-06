from flask import Flask
from flask_login import LoginManager
from db import init_db
from db_init import create_tables
import os

login_manager = LoginManager()
login_manager.login_view = "auth.login"

def create_app():
app = Flask(**name**)

```
app.config["SECRET_KEY"] = "secret"

# Initialize database
init_db(app)

# Create tables only if not exist
create_tables(app)

# Login manager
login_manager.init_app(app)

from models.models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Register blueprints
from routes.auth import auth_bp
app.register_blueprint(auth_bp)

return app
```

app = create_app()

if **name** == "**main**":
port = int(os.environ.get("PORT", 10000))
app.run(host="0.0.0.0", port=port)
