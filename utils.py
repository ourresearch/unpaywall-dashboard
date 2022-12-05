from app import app, db
from auth.models import User


def create_user(email, name, password):
    """Create a new user."""
    with app.app_context():
        user = User(email=email, name=name)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        print("Created user: {}".format(user))
