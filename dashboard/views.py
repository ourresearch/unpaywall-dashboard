from flask import Blueprint, render_template
from flask_login import login_required, logout_user, current_user, login_user

dashboard_blueprint = Blueprint("dashboard", __name__)


@dashboard_blueprint.route("/")
@login_required
def dashboard():
    return render_template("index.html", current_user=current_user)
