from flask_wtf import Form
from wtforms import TextField
from wtforms.validators import DataRequired, length


class InstagramAnalyzer(Form):
    instagram_analyze = TextField(
        'Analyze', validators=[DataRequired(), length(min=2)])
