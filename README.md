# Instagram Scraper - from IPython to Flask

Heroku [link](http://instagram-scrape.herokuapp.com/) to the web app.

Welcome!

**Today we’ll take an IPython Notebook that pulls data from the Instagram API and then analyzes the data via Pandas and convert it into a Flask app that also displays charts and graphs using matplotlib based on the data analysis.**

ADD IMAGE

*This is a guest post by ____, a Python developer...*

In the first two parts, we'll begin by structuring our working environment and in the third part we'll work on porting the back-end logic from the IPython Notebook to the Flask application:

1. *Part One*: Setup the local development environment along with the basic Flask app.
1. *Part Two*: Setup the production environment on Heroku and push the current application to the cloud.
1. *Part Three*: Add in the back-end logic to access the Instagram API, process the data with Pandas/Numpy, and create the charts with matplotlib.

We're excited to present how to take an IPython Notebook, containing all of our data work, and strip out the relevant parts to build out the Flask back-end and then add a nice front-end so that our work can be displayed in a browser for the world to see.

> Keep in mind that this is a low-level tutorial for those looking to get familiar with Flask, understand the development workflow, convert code from IPython to Flask, and deploy a basic app to Heroku.

Enjoy!

## Part One: Local Development

Let's quickly setup a basic environment for local development utilizing the following tools - [virtualenv](http://www.virtualenv.org/en/latest/), [Flask](http://flask.pocoo.org/), and [Heroku](https://heroku.com)

Make a project directory and create/activate a virtualenv:

```sh
$ mkdir instagram_scraper && cd instagram_scraper
$ virtualenv venv
$ source venv/bin/activate
```

> **Remember**: The virtualenv allows us to neutralize our environment and work exclusively with the tools necessary for our app.

Install Flask and create the *requirements.txt* file, which will become important later when Heroku looks to install the necessary libraries when we deploy to production:

``` sh
$ pip install Flask==0.10.1
$ pip freeze > requirements.txt
```

Add a local Git repo along with a basic *README.md* file:

```sh
$ git init
$ echo "# instagram_scraper" >> README.md
```

Now add a *.gitignore* file:

```
.DS_Store
*.pyc
venv
```

Then add a remote Git repo on Github and commit your changes locally before pushing your current code up to Github. It's a good practice to frequently commit your code locally and push your changes to GitHub so that you can easily pull up a previous version of you code in case of a mistake.

So far so good. Now lets create our basic project structure.

```sh
$ touch run.py
```

Your project directory should now look like this:


```sh
├── README.md
├── run.py
└── requirements.txt
```

Open up *run.py* in your favorite editor (like [Sublime Text 3](https://realpython.com/blog/python/setting-up-sublime-text-3-for-full-stack-python-development/)) and add the following code:

```python
from flask import Flask
app = Flask(__name__)


@app.route('/')
def main():
    return "Python Instagram Scraper"

if __name__ == '__main__':
    app.run()
```

Run the app locally:

```sh
$ python run.py
```

You should see the displayed text of "Python Instagram Scraper" in action at [http://localhost:5000/](http://localhost:5000/). Once done, kill the server.

Now let's get Heroku up and running!

## Part Two: Setup Heroku

Given you have the Heroku [Toolbelt](https://toolbelt.heroku.com/) installed, follow the steps below to get the app up and running. *For more info on using Python with Heroku, check out the official [Heroku documenation](https://devcenter.heroku.com/articles/getting-started-with-python#introduction).

Create a Procfile and add the following code:

```sh
$ echo "web: gunicorn run:app" >> Procfile
```

Basically, you name one process/service per line that you want to run on Heroku; currently we just want to run our app.

Make sure install gunicorn and add it to *requirements.txt*:

```sh
$ pip install gunicorn==19.3.0
$ pip freeze > requirements.txt
```

Lets create our app on Heroku and initialize it:

```sh
$ heroku create
```

Then commit and push your code up to Heroku:

```sh
$ git add -A
$ git commit -m "first commit"
$ git push heroku master
```

Checkout your app:

```sh
$ heroku open
```

Now to the fun part!

## Part Three: Back-End Logic

Lets create new folders and python files inside our directory. Follow the structure of our app below:

```
sh
$ mkdir instagram_scraper_app && cd instagram_scraper_app
$ touch __init__.py instagram_analyze.py instagram_graphs.py keys.py forms.py config.py
$ mkdir templates && cd templates
$ touch instagram_scraper.html index.html _base.html
$ cd ..
$ mkdir static && cd static
$ mkdir css js && cd css
$ touch main.css
$ cd ../../..
```

Your app's structure should now look like:

```sh
├── Procfile
├── README.md
├── instagram_scraper_app
│   ├── __init__.py
│   ├── config.py
│   ├── forms.py
│   ├── instagram_analyze.py
│   ├── instagram_graphs.py
│   ├── keys.py
│   ├── static
│   │   ├── css
│   │   │   └── main.css
│   │   └── js
│   └── templates
│       ├── _base.html
│       ├── index.html
│       └── instagram_scraper.html
├── requirements.txt
└── run.py
```

Next, we'll work on creating our Instagram scraper within *instagram_analyze.py*. Our code will crawl/iterate through each Instagram page via the pagination links. We could use the API to grab data, but it's capped at 5,000 post [limit](https://instagram.com/developer/limits/) per 24-hour period.

EDITED UP TO HERE - michael

## Part Three-A: Setting Up .gitignore

The file ".gitignore" gets picked up by GitHub when pushing changes up. The folders/files mentioned in .gitignore get hidden from the public.

Typically, it's a good idea to mention all the files that you want hidden, especially keys or tokens inside .gitignore.

keys.py will be treated a little differently from other files when hiding it using .gitigonre because otherwise heroku will not see the keys.py and our instagram data will not be generated. Right now, lets add these files to .gitignore:

###### .gitignore
```
venv
*.pyc
*.db
env.sh
```

Create an env.sh file inside our root directory:

```
$ touch env.sh
```
>Leave env.sh empty for now. That's where we will keep our keys and tokens hidden from everyone. This info will be exported into the keys.py. You'll see how we do this later.


## Part Three-B: Templates, HTML and CSS

Click [here](https://raw.githubusercontent.com/odubno/instagram_scraper/master/instagram_scraper_app/static/css/bootstrap.min.css) and copy/paste this css code into bootstrap.min.css

Click [here](https://raw.githubusercontent.com/odubno/instagram_scraper/master/instagram_scraper_app/static/css/main.css) and copy paste this code into main.css

Our css will format the contents of the page and we'll gain control of its display.

Our _base.html will be the standard layout for all of our HTML pages. As opposed to typing out our css for each HTML page we could simply pull it in from our base:

###### _base.html
```
<!DOCTYPE html>
<html>
  <head>
    <meta charset='utf-8'>
    <title>Instagram Scraper</title>

    <!-- meta -->
    <meta name='description' content=" ">
    <meta name='author' conten=" ">
    <meta name='viewport' content="width=device-width,initial-scale=1">

    <!-- styles -->
    <link href="{{url_for('static', filename='./css/bootstrap.min.css')}}" rel="stylesheet" media="screen">

    <link href="{{url_for('static', filename='./css/main.css')}}" rel="stylesheet" media="screen">


    {% block css %}{% endblock %}
  </head>
  <body>

    <div class="container">

      <br>

      <!-- messages -->
      {% with messages = get_flashed_messages(with_categories=true) %}
      {% if messages %}
      <div class="row">
        <div class="col-md-12">
          {% for category, message in messages %}
          <div class="alert alert-{{ category }}">
            <a class="close" title="Close" href="#" data-dismiss="alert">&times;</a>
            {{message}}
          </div>
          {% endfor %}
        </div>
      </div>
      {% endif %}
      {% endwith %}

      <!-- child template -->
      {% block content %}{% endblock %}

      <br>

      <!-- errors -->
      {% if error %}
        <p class="error"><strong>Error:</strong> {{ error }}</p>
      {% endif %}

    </div>

  </body>
</html>
```
Now that we have the _base.html figured out lets pull the base into our other HTML files.

Configure the index.html. This form will display the form field for entry and a placeholder to indicate what should be entered. In our case a hashtag. The userinput will then be pulled into the python script and scrape the Instagram API.

###### index.html
```
{% extends "_base.html" %}
{% block content %}

<h1>Python Instagram Scraper</h1>
<br>

<form class="" role="form" method="post" action="">
  {{ form.csrf_token }}
  <p>
    {{ form.instagram_scrape(class="form-control input-lg", placeholder="Enter Hashtag")}}
    <span class="error">
      {% if form.instagram_scrape.errors %}
        {% for error in form.instagram_scrape.errors %}
          {{ error }}
        {% endfor %}
      {% endif %}
    </span>
  </p>
  <button class="btn btn-default btn-lg" type="submit">Analyze!</button>
</form>

<br>

{% endblock %}
```

instagram_scraper.html will render the display of our analysis. The input will be what the user had passed in the form and the filename will be our graphs.

###### instagram_scraper.html
```
{% extends "_base.html" %}

{% block content %}

    <h2>Hashtag:</h2>
    <div class="well">{{ input }}</div>


    <h2>Analysis:</h2>

    <iframe src={{ filename }} frameborder="0" align="middle" height="600" width="650"</iframe>


    <h3><a href="/">Again?</a></h3>



{% endblock %}
```
## Part Three-C: Instagram API

Now that we have the HTML and CSS figured out lets take a look at the Instagram API.

Before any work in Python, you’ll need to first register a new client with Instagram.  Once you’re logged into Instagram, you can do that [here](https://instagram.com/developer/clients/register/).An arbitrary URL and URI can be used for the sake of this exercise.

>Once you’ve registered a client, you should have your own Client ID and Secret. These will be used to get connected to the API. With that, we can now get to Python.

Store your credentials in env.sh:

###### env.sh
```
#!/bin/bash

export "client_id=768fcff36c95eb08506bae8a9caffa3"
export "secret=54efcdaed8f64673bc96b4e28c39e8b2"
export "access_token=13521778.765fdf1.f05c803b0a9d4c7dbac20060e0c2bc8d"

```
>The above keys are made up and will not work, but these should reflect what you have.

Let's modify the keys.py to pull in our instagram API credentials:

###### keys.py
```
import os

CLIENT_ID = os.environ['client_id']
# SECRET = os.environ['secret']
# ACCESS_TOKEN = os.environ['access_token']
```

>SECRET and ACCESS is commented out as it is not necessary for the work we're doing.

Our env.sh file is hidden within .gitignore.

Just reiterating. Running:

```
sh
$ source venv/bin/activate
```
activates our working environment along with all of our dependencies to run our app.

Now that our keys and tokens are hidden, to activate our keys to be used inside out envirnment we have to run:

```
sh
$ source env.sh
```
>This command will execute and run our Instagram credentials.

Additional instructions will be given below, in order to keep keys hidden when exporting the app to Heroku.

config.py will establish the url and the features we will be pulling from Instagram.

###### config.py
```
WTF_CSRF_ENABLED = True
SECRET_KEY = "pass"
base_url = "https://api.instagram.com/v1"
cols = [
'user.username',
'caption.text',
'tags',
'comments.count',
'likes.count',
'filter',
'type',
'created_time',
'user.full_name',
'user.id',
'link',
'location.latitude',
'location.longitude'
]
```

forms.py validates user input and makes sure that data is entered and the length of the input is no less than 2 characters.

###### forms.py
```
from flask_wtf import Form
from wtforms import TextField
from wtforms.validators import DataRequired, length

class InstagramScraper(Form):
  instagram_scrape = TextField(
    'Scrape', validators=[DataRequired(), length(min=2)])
```

The fun begins. Here, we'll be pulling in our keys.py, config.py, forms.py and pre-packaged Python modules to help us with scraping Instagram, cleaning of the data using json, Pandas and displaying the results in a pandas DataFrame.

>Make sure that keys.py, config.py and forms.py are A-OK.

Our first function of the script grabs the url


Below, you'll find that we're using "pagination" and "next_url" to iterate through Instagram data and pull in more than 33 posts.

>Instagram limits us to only 33 of its most recent posts per search.

We do some cleaning of the data and return it in a DataFrame.


###### instagram_analyze.py
```
from config import *
from forms import InstagramScraper
import requests
import json
from pandas.io.json import json_normalize
from keys import *
import pandas as pd
import datetime

#returns str(requests.get(url).json()['pagination']['next_url'] for a specified url
def get(url):
    r = requests.get(url)
    j = r.json()
    if 'pagination' in j:
        try:
            pagination = j['pagination']
            if 'next_url' in pagination:
                try:
                    next_url = pagination['next_url']
                    return str(next_url)
                except Exception, e:
                    return str(e)
        except Exception, e:
            return str(e)

#replaces '.' with spaces in selected column titles of a specified dataframe
#cols contained in config
def df_slice(df, cols):
    new_cols = list()
    new_df = pd.DataFrame()
    for col in cols:
        if col in df:
            new_cols.append(col)
    new_df = df[cols]
    return new_df.rename(columns=lambda x: x.replace('.', ' ').title())

#returns dataframe; iterates through and compiles a dataframe of n pages of instagram data from a specified url
def instagram_scraper(query, n):
    url = '{0}/tags/{1}/media/recent?client_id={2}&count=30'.format(base_url, query, client_id)
    urls = list()
    results = list()

    urls.append(str(url))

    for _ in range(n):
        x = get(url)
        urls.append(str(x))
        url = get(x)

    for url in urls:
        r = requests.get(url)
        j = r.json()
        if 'data in j':
            try:
                data = j['data']
                df_instance = json_normalize(data)
                results.append(df_instance)
            except Exception, e:
                return 'Error: Could not find data.', str(e)

    df = pd.DataFrame().append(results)
    df = df.reset_index()
    df = df.drop('index',axis=1)

#further df cleans
    df['created_time'] = [x.replace(x, datetime.datetime.fromtimestamp(int(str(x))).strftime('%Y-%m-%d %H:%M:%S')) for x in df['created_time']]
    df = df_slice(df, cols) #applies df_slice to slice dataframe; selects columns specified in config, cleans column titles

    return df
```

>I'm not explicitly mentioning IPython Notebook, but know that I tested all this code in IPython Notebook before moving it over to development.

instagram_graphs.py is formated to work with the DataFrame we have in instagram_analyze.py and create graphs. We will pull both functions together in our __init__.py


###### instagram_graphs.py
```
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import matplotlib.pyplot as plt
from pandas import read_csv
import pandas as pd

from matplotlib.figure import Figure

# Displays all the graphs

def instagram_graph(instagram_scraped):

    fig = plt.figure(figsize=(8,6))

    ax1 = plt.subplot2grid((3,3), (0,0), colspan=3, rowspan=1)
    instagram_scraped['Comments Count'].plot(kind='bar', alpha=.55)
    plt.title("Total Comments Count")


    ax2 = plt.subplot2grid((3,3), (1,0), colspan=3, rowspan=1)
    instagram_scraped['Likes Count'].plot(kind='bar', alpha=.55)
    plt.title("Total Likes Count")


    ax3 = plt.subplot2grid((3,3), (2,0), colspan=3, rowspan=1)
    plt.hist(instagram_scraped['Likes Count'])
    plt.title('Distribution of Likes on Instagram Posts', fontsize=20)
    plt.xlabel('Amount of Posts', fontsize=18)
    plt.ylabel('Likes', fontsize=16)
    fig_size = plt.rcParams["figure.figsize"]

    fig.tight_layout()
```

Here we create our routes and all of our files get pulled together and rendered to display in the app.

instagram_analyze() scrapes Instagram, cleans the data and outputs it in a DataFrame.

That DataFrame is pulled into instagram_graphs() and it outputs a matplotlib graph.

The output, using matplotlib, is a png file. Here we use StringIO to render the graph and have it displayed as a png file in the app.

###### __init__.py
```
from flask import Flask, render_template, request, flash, \
  flash, url_for, redirect, make_response, send_file

from instagram_analyze import *
from instagram_graphs import *

import StringIO
from cStringIO import StringIO


app = Flask(__name__)
app.config.from_object('instagram_scraper_app.config')


#routes


@app.route('/', methods=['GET','POST'])
def main():
  form = InstagramScraper(request.form)
  if form.validate_on_submit():
    text = form.instagram_scrape.data
    return redirect(url_for('instagram_scrape', user_input=text))
  return render_template('index.html', form=form)


@app.route("/instagram_scrape/<user_input>") # 1
def instagram_scrape(user_input):

  return render_template(
    'instagram_scraper.html',
    input=user_input,
    filename=user_input+".png" # 2
    )

"""
The beginning of the route @app.route("/instagram_scrape/<user_input>") picks
up what the user had passed as a hashtag. The user_input is then passed in for
filename with a ".png" ending.

The route ending is the user_input.
Both routes have "/instagram_scrape/..." this causes the response route to render
the user_input with the ".png" ending
@app.route("/instagram_scrape/<image_name>.png")


"""

@app.route("/instagram_scrape/<image_name>.png") # 3
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
```
Our final step is to simply change the run.py to:

```
import os
from instagram_scraper_app import app

if __name__ == '__main__':
  app.run(debug=True)
```
>This script imports our app and excecutes it in the browser.

Before running our app we'll have to pip install a few dependencies to run it.

> Make sure that you're inside your virtual environment.

```
sh
$ source venv/bin/activate
```

Let's pip install the dependencies:

```
sh
$ pip install flask_wtf requests pandas matplotlib simplejson python-instagram
```

Let's run it locally:

```
sh
$ python run.py
```

Cool. Hopefully that works.

Lets push up our final changes to GitHub and Heroku.

Before we do that we have to upload our dependencies to our requirements.txt:

```
sh
$ pip freeze > requirements.txt
```
Followed by the add/commit and push structure:

```
sh
$ git add .
$ git commit -m "final push"
$ git push heroku master

> Pushing up dependencies to Heroku will take some time. Be patient.

```
And one final thing to take care of our hidden keys is to run the code below in our terminal:

```
sh
heroku config:set client_id=768fcff36c95eb08506bae8a9caffa3
```
>Running the above command will configure Heroku to use the necessary key to run our app. Read more about it [here](https://devcenter.heroku.com/articles/config-vars). The above client id is made up.

Type:
```
sh
$ heroku open
```
to open the app in the browser


In case the dependencies fail to be pushed up or you hit a timeout:

```
sh
$ pip uninstall matplotlib
$ pip uninstall pandas
$ pip freeze > requirements.txt
```
Push to heroku again.

Once it works:

```
sh
$ pip install matplotlib
$ pip freeze > requirements.txt
```
Push to Heroku again.

Then:

```
sh
$ pip install pandas
$ pip freeze > requirements.txt
```
Push to Heroku one more time and run:

```
sh
$ heroku open
```
> Something about pushing up all your dependencies at once causes Heroku to crash or timeout. Do it piece by piece.

Please add you questions/comments below. Thank you!!!




