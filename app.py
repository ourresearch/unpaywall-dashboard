import os

from flask import Flask

from extensions import db, login_manager
import auth
import dashboard

app = Flask(__name__)

uri = os.environ.get("DATABASE_URL")
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)

app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev")
app.config["SQLALCHEMY_DATABASE_URI"] = uri
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.register_blueprint(auth.views.auth_blueprint)
app.register_blueprint(dashboard.views.dashboard_blueprint)

db.init_app(app)
login_manager.init_app(app)

if __name__ == "__main__":
    app.run()
