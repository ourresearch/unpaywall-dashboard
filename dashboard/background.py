import subprocess

from app import rq


@rq.job
def refresh_doi_background(doi):
    result = subprocess.run(
        f"heroku run python queue_pub.py --method=refresh --id='{doi}' --app articlepage",
        shell=True,
        capture_output=True,
    )
    output = result.stdout.decode("utf-8")
    return output
