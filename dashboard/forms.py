from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class DOIForm(FlaskForm):
    doi = StringField(
        "DOI", validators=[DataRequired()], render_kw={"placeholder": "10.1234/1234"}
    )
    submit = SubmitField("Submit")
