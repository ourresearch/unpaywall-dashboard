from sqlalchemy.dialects.postgresql import JSONB

from app import db


class OAManual(db.Model):
    __bind_key__ = "unpaywall_db"
    __tablename__ = "oa_manual"

    id = db.Column(db.Integer, primary_key=True)
    doi = db.Column(db.Text, unique=True)
    response_jsonb = db.Column(JSONB)


class JournalOAYearOverride(db.Model):
    __bind_key__ = "unpaywall_db"
    __tablename__ = "journal_oa_year_override"

    issn_l = db.Column(db.Text, primary_key=True)
    oa_year = db.Column(db.Integer)
