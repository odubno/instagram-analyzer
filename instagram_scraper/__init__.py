from flask import Flask, render_template, request, flash, \
  flash, url_for, redirect

from instagram_analyze import * 

app = Flask(__name__)
app.config.from_object('instagram_scraper.config')


#routes 

@app.route('/', methods=['GET','POST'])
def main():
  form = InstagramScraper(request.form)
  if form.validate_on_submit():
    text = form.instagram_scrape.data
    return redirect(url_for('instagram_scrape', user_input=text))
  return render_template('index.html', form=form)


@app.route('/instagram_search/<user_input>')
def instagram_scrape(user_input):
  instagram_scraped = instagram_scraper(user_input)
  return render_template(
    'instagram_scraper.html',
    input=user_input,
    output=instagram_scraped
    )

@app.route('/about')
def home():
  return render_template('about.html')
