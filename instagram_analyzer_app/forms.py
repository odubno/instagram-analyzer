from flask_wtf import Form
from wtforms import TextField
from wtforms.validators import DataRequired, length


class InstagramAnalyzerForm(Form):
    keyword = TextField(
        'Keyword',
        validators=[DataRequired(), length(min=2)]
    )