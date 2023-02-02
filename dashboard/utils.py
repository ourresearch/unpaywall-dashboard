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


def insecure_url(result):
    if result and "best_oa_location" in result and result["best_oa_location"]:
        if (
            "url" in result["best_oa_location"]
            and result["best_oa_location"]["url"]
            and result["best_oa_location"]["url"].startswith("http://")
        ):
            return result["best_oa_location"]["url"]
        elif (
            "url_for_pdf" in result["best_oa_location"]
            and result["best_oa_location"]["url_for_pdf"]
            and result["best_oa_location"]["url_for_pdf"].startswith("http://")
        ):
            return result["best_oa_location"]["url_for_pdf"]
        elif (
            "url_for_landing_page" in result["best_oa_location"]
            and result["best_oa_location"]["url_for_landing_page"]
            and result["best_oa_location"]["url_for_landing_page"].startswith("http://")
        ):
            return result["best_oa_location"]["url_for_landing_page"]
    return None
