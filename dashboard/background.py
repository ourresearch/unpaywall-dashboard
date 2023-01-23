import os
import time
import heroku3
import requests

from app import rq


@rq.job
def refresh_doi_background(doi):
    # get original version of the record
    url = f"https://api.unpaywall.org/v2/{doi}?email=support@unpaywall.org"
    r = requests.get(url)
    old = r.json()

    # refresh the record
    HEROKU_API_KEY = os.environ.get("HEROKU_API_KEY")
    heroku_conn = heroku3.from_key(HEROKU_API_KEY)
    app = heroku_conn.apps()["articlepage"]
    command = f"python queue_pub.py --method=refresh --id='{doi}'"
    output = app.run_command(command, printout=True)

    time.sleep(5)

    # get the new version of the record
    r = requests.get(url)
    new = r.json()

    # compare the two
    is_changed = False
    if old.get("best_oa_location") and not new.get("best_oa_location"):
        is_changed = True

    if old.get("best_oa_location") and new.get("best_oa_location"):
        for k, v in old.get("best_oa_location", {}).items():
            if k != "updated" and new["best_oa_location"].get(k) != v:
                is_changed = True
    if old.get("oa_status") != new.get("oa_status"):
        is_changed = True

    if old.get("is_oa") is True and new.get("is_oa") is False:
        switched_to_closed = True
    elif old.get("is_oa") is False and new.get("is_oa") is True:
        switched_to_open = True
    else:
        switched_to_closed = False
        switched_to_open = False

    # create result
    result = {
        "is_changed": is_changed,
        "switched_to_closed": switched_to_closed,
        "switched_to_open": switched_to_open,
        "log": output[0],
    }
    return result
