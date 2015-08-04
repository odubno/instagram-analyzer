from cStringIO import StringIO
from flask import Flask, render_template, request, \
  flash, url_for, redirect, make_response, send_file
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import matplotlib.pyplot as plt


from instagram_analyze import instagram_scraper
from instagram_graphs import instagram_graph
from forms import InstagramScraper


app = Flask(__name__)
app.config.from_object('instagram_scraper_app.config')


# routes


@app.route('/', methods=['GET', 'POST'])
def main():
    form = InstagramScraper(request.form)
    if form.validate_on_submit():
        text = form.instagram_scrape.data
        return redirect(url_for('instagram_scrape', user_input=text))
    return render_template('index.html', form=form)


@app.route("/instagram_scrape/<user_input>")  # 1
def instagram_scrape(user_input):

    return render_template(
        'instagram_scraper.html',
        input=user_input,
        filename=user_input+".png"  # 2
    )

"""
The beginning of the route @app.route("/instagram_scrape/<user_input>") picks
up what the user had passed as a search. ".png" is then appended to user_input to create
the image title. 

The ending of the url will show up as the input and reference the filename.
Both routes have "/instagram_scrape/..." this causes the response route to render
the user_input with the ".png" ending
@app.route("/instagram_scrape/<image_name>.png")


"""


@app.route("/instagram_scrape/<image_name>.png")  # 3
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

    return response


@app.route('/about')
def home():
    return render_template('about.html')
