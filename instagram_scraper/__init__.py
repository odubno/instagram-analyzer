from flask import Flask, render_template, request, flash, \
  flash, url_for, redirect, make_response

from instagram_analyze import * 

from cStringIO import StringIO
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import matplotlib.pyplot as plt
from pandas import read_csv
import pandas as pd

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


# @app.route('/instagram_search/<user_input>')
# def instagram_scrape(user_input):
#   instagram_scraped = instagram_scraper(user_input)
#   return render_template(
#     'instagram_scraper.html',
#     input=user_input,
#     output=instagram_scraped
#     )


@app.route('/instagram_scrape/<user_input>')
def instagram_scrape(user_input):
  instagram_scraped = instagram_scraper(user_input)

  # defining the graph
  plt.hist(instagram_scraped['likes_count'])

  # rendering matplotlib image to Flask view
  canvas = FigureCanvas(plt.gcf())
  output = StringIO()
  canvas.print_png(output)
  response = make_response(output.getvalue())
  response.mimetype = 'image/png'

  return response


# @app.route('/images/<user_input>')
# def images(user_input):
#   return render_template("instagram_scraper.html") 


# @app.route('/fig/<user_input>')
# def fig(user_input):
#   fig = instagram_scraper(user_input)

#   # defining the graph
#   plt.hist(instagram_scrape['likes_count'])

#   # rendering matplotlib image to Flask view
#   img = StringIO()
#   fig.savefig(img)
#   img.seek(0)

#   return send_file(img, mimetype='image/png')
  





@app.route('/about')
def home():
  return render_template('about.html')
