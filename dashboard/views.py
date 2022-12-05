import subprocess

from flask import Blueprint, render_template, request
from flask_login import login_required, current_user

from dashboard.forms import DOIRefreshForm


dashboard_blueprint = Blueprint("dashboard", __name__)


@dashboard_blueprint.route("/")
@login_required
def dashboard():
    return render_template("index.html", current_user=current_user)


@dashboard_blueprint.route("/refresh-doi", methods=["GET", "POST"])
@login_required
def refresh_doi():
    form = DOIRefreshForm()
    if form.validate_on_submit():
        doi = form.doi.data
        if doi:
            # refresh doi
            result = subprocess.run(
                f"heroku run python queue_pub.py --method=refresh --id='{doi}' --app articlepage",
                shell=True,
                capture_output=True,
            )
            output = result.stdout.decode("utf-8")
            return render_template(
                "refresh_doi.html", output=output, current_user=current_user, form=form
            )
    return render_template("refresh_doi.html", current_user=current_user, form=form)
