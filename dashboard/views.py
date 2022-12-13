import time
import re

from flask import Blueprint, render_template, redirect, url_for, Markup, request, jsonify
from flask_login import login_required, current_user
import requests
from rq.queue import Queue
from rq.job import Job
from rq.registry import StartedJobRegistry, FinishedJobRegistry, FailedJobRegistry

from app import rq
from dashboard.background import refresh_doi_background
from dashboard.forms import DOIForm


dashboard_blueprint = Blueprint("dashboard", __name__)


@dashboard_blueprint.route("/")
@login_required
def dashboard():
    form = DOIForm()
    doi = request.args.get("doi")
    result = None
    if doi:
        r = requests.get(
            f"https://api.unpaywall.org/v2/{doi}?email=support@unpaywall.org"
        )
        result = dict(r.json())
    return render_template(
        "index.html", current_user=current_user, form=form, result=result, doi=doi
    )


@dashboard_blueprint.route("/refresh-doi", methods=["GET", "POST"])
@login_required
def refresh_doi():
    form = DOIForm()
    if form.validate_on_submit():
        refresh_doi_background.queue(
            form.doi.data, description=form.doi.data, result_ttl=5000
        )
        time.sleep(0.3)
        return redirect(url_for("dashboard.refresh_doi"))
    queue = Queue("default", connection=rq.connection)
    started_jobs = StartedJobRegistry("default", connection=rq.connection)
    finished_jobs = FinishedJobRegistry("default", connection=rq.connection)
    failed_jobs = FailedJobRegistry("default", connection=rq.connection)
    job_ids = (
        started_jobs.get_job_ids()
        + queue.get_job_ids()
        + finished_jobs.get_job_ids()
        + failed_jobs.get_job_ids()
    )
    results = []
    for job_id in job_ids:
        job = Job.fetch(job_id, connection=rq.connection)
        if job.result:
            try:
                result = re.sub("\d+:", "<br>", job.result)
                result = result.replace("<meta http-equiv=", "")
                result = Markup(result)
            except TypeError:
                result = job.result
        else:
            result = None
        results.append(
            {
                "doi": job.description,
                "status": job.get_status(),
                "result": result,
                "timestamp": job.enqueued_at,
            }
        )
        results = sorted(results, key=lambda d: d['timestamp'], reverse=True)
    return render_template(
        "refresh_doi.html", current_user=current_user, form=form, results=results
    )


@dashboard_blueprint.route("/refresh-doi/<path:doi>")
@login_required
def start_fresh(doi):
    job = refresh_doi_background.queue(doi, description=doi, result_ttl=5000)
    return jsonify({"job_id": job.get_id()})


@dashboard_blueprint.route("/refresh-status/<path:job_id>")
@login_required
def refresh_status(job_id):
    job = Job.fetch(job_id, connection=rq.connection)
    if job.result and job.is_finished:
        result = job.result
    else:
        result = None
    return jsonify(
        {
            "status": job.get_status(),
            "result": result,
            "timestamp": job.enqueued_at,
        }
    )