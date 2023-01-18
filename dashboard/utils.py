from dashboard.models import OAManual


def is_doi_manually_closed(doi):
    if doi:
        doi = doi.strip().replace("https://doi.org/", "")
        oa_manual = OAManual.query.filter_by(doi=doi).first()
        if oa_manual and oa_manual.response_jsonb == {}:
            return True
        else:
            return False
    return False
