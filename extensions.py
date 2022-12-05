from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_rq2 import RQ

db = SQLAlchemy()
login_manager = LoginManager()
rq = RQ()
