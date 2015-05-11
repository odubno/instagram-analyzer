from flask import Flask, render_template, request, flash, \
  flash, url_for, redirect, make_response, send_file

from instagram_analyze import * 
from instagram_graphs import *

import StringIO
from cStringIO import StringIO


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


@app.route("/instagram_scrape/<user_input>")
def instagram_scrape(user_input):

  return render_template(
    'instagram_scraper.html',
    input=user_input,
    filename=user_input+".png"
    )


@app.route("/instagram_scrape/<image_name>.png")
def image(image_name):
  # pulls in the scraper and creates the DataFrame
  instagram_scraped = instagram_scraper(image_name, 0)

  # formats the DataFrame to display plots 
  instagram_graph(instagram_scraped)


  # rendering matplotlib image to Flask view
  canvas = FigureCanvas(plt.gcf())
  output = StringIO()
  canvas.print_png(output)
  # make_response converts the return value from a view 
  # function to a real response object that is an instance 
  # of response_class.
  response = make_response(output.getvalue())

  response.mimetype = 'image/png'
  response.headers["Content-Type"] = ("image/png; filename=data.png")

  return response


@app.route('/about')
def home():
  return render_template('about.html')
