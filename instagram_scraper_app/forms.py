from flask_wtf import Form
from wtforms import TextField
from wtforms.validators import DataRequired, length


class InstagramScraper(Form):
    instagram_scrape = TextField(
        'Scrape', validators=[DataRequired(), length(min=2)])
