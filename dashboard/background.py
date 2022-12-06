import os
import heroku3

from app import rq


@rq.job
def refresh_doi_background(doi):
    HEROKU_API_KEY = os.environ.get("HEROKU_API_KEY")
    heroku_conn = heroku3.from_key(HEROKU_API_KEY)
    app = heroku_conn.apps()["articlepage"]
    command = f"python queue_pub.py --method=refresh --id='{doi}'"
    output = app.run_command(command, printout=True)
    return output
