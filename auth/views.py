from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required, logout_user, current_user, login_user
from auth.forms import LoginForm, CreateUserForm
from auth.models import User

from extensions import db, login_manager

auth_blueprint = Blueprint("auth", __name__)


@auth_blueprint.route("/create-user", methods=["GET", "POST"])
def create_user():
    return render_template("auth/create_user.html")


@auth_blueprint.route("/login", methods=["GET", "POST"])
def login():
    # Bypass if user is logged in
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.dashboard"))

    form = LoginForm()
    # Validate login attempt
    if form.validate_on_submit():
        print("validated")
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(password=form.password.data):
            login_user(user)
            return redirect(url_for("dashboard.dashboard"))
        flash("Invalid username/password combination")
        return redirect(url_for("auth.login"))
    return render_template("auth/login.html", form=form)


@auth_blueprint.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))


@login_manager.user_loader
def load_user(user_id):
    if user_id is not None:
        return User.query.get(user_id)
    return None


@login_manager.unauthorized_handler
def unauthorized():
    """Redirect unauthorized users to Login page."""
    flash("You must be logged in to view that page.")
    return redirect("/login")
