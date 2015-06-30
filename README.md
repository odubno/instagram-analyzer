# Instagram Analyzer - from IPython to Flask

Welcome!

**Today we’ll take an IPython Notebook that pulls data from the Instagram API and then analyzes the data via Pandas and convert it into a Flask app that also displays charts and graphs using matplotlib based on the data analysis.**

(/instagram_scraper_app/static/img/01_instagram_analyzer.png "Landing Page")

*This is a guest post by ____, a Python developer...*

In the first two parts, we'll begin by structuring our working environment and in the third part we'll work on porting the back-end logic from the IPython Notebook to the Flask application:

1. *Part One*: Setup the local development environment along with the basic Flask app.
1. *Part Two*: Setup the production environment on Heroku and push the current application to the cloud.
1. *Part Three*: Add in the back-end logic to access the Instagram API, process the data with Pandas/Numpy, and create the charts with matplotlib.

We're excited to present how to take an IPython Notebook, containing all of our data work, and strip out the relevant parts to build out the Flask back-end and then add a nice front-end so that our work can be displayed in a browser for the world to see.

> Keep in mind that this is a low-level tutorial for those looking to get familiar with Flask, understand the development workflow, convert code from IPython to Flask, and deploy a basic app to Heroku.

Enjoy!

ADD ALL DEPENDECIES AND VERSIONS HERE
DO BETTER JOB OF EXPLAINING HOW TO GO FROM IPYTHON TO FLASK. START WITH BETTER INTRO OF WHAT'S HAPPENING IN THE IPYTHON NOTEBOOK. START WITH IPYTHON, DESCRIBING WHAT IT DOES AND THEN EXPLAIN WHAT YOU'RE GOING TO CREATE. THIS IS THE "WHAT" and "WHY" THE BLOG POST IS THE "HOW".

Dependencies for the app:
```
Flask==0.10.1
Flask-WTF==0.11
Jinja2==2.7.3
MarkupSafe==0.23
WTForms==2.0.2
Werkzeug==0.10.4
gunicorn==19.3.0
httplib2==0.9.1
itsdangerous==0.24
matplotlib==1.4.3
mock==1.0.1
nose==1.3.6
numpy==1.9.2
pandas==0.16.1
pyparsing==2.0.3
python-dateutil==2.4.2
python-instagram==1.3.1
pytz==2015.2
requests==2.6.2
simplejson==3.6.5
six==1.9.0
wsgiref==0.1.2
```

Follow this [link](https://github.com/odubno/instagram_scraper/blob/master/IPython_Notebook_Files/instagram_analyze_json_DataFrame.ipynb) to see our first IPython Notebook, where we use our CLIENT_ID to pull data from Instagram, convert it into json and pull it into a pandas DataFrame. Super easy code to follow.

Follow this [link](https://github.com/odubno/instagram_scraper/blob/master/IPython_Notebook_Files/instagram_analyze_Data_Cleaning.ipynb) to see the cleaning that we did to our data. Here we clean the date field, select the columns we want to work with and output it back into a pandas Data Frame.






## Structure

Let's quickly setup a basic environment for local development utilizing the following tools - [virtualenv](http://www.virtualenv.org/en/latest/), [Flask](http://flask.pocoo.org/), and [Heroku](https://heroku.com)

Make a project directory and create/activate a virtualenv:

```sh
$ mkdir instagram_analyzer && cd instagram_analyzer
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
$ echo "# Instagram Analyzer" >> README.md
```

Now add a *.gitignore* file to hide certain files and folders from the public:

```
.DS_Store
*.pyc
venv
```

> It's good practice to add system files (like *.DS_Store), dependency folers (like "venv"), and any sensitive information (more on this later) to the *.gitignore* file.

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
    return "Python Instagram Analyzer"

if __name__ == '__main__':
    app.run()
```

Run the app locally:

```sh
$ python run.py
```

You should see the displayed text of "Python Instagram Analyzer" in action at [http://localhost:5000/](http://localhost:5000/). Once done, kill the server.

Now let's get Heroku up and running!

## Heroku Setup

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

## More Structure

Lets create new folders and Python files inside our directory.

### Setup

Follow the structure of our app below:

```
sh
$ mkdir instagram_analyzer_app && cd instagram_analyzer_app
$ touch __init__.py instagram_analyze.py instagram_graphs.py keys.py forms.py config.py
$ mkdir templates && cd templates
$ touch instagram_analyzer.html index.html _base.html
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
├── instagram_analyzer_app
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
│       └── instagram_analyzer.html
├── requirements.txt
└── run.py
```

Next, we'll work on creating our Instagram analyzer within *instagram_analyze.py*. Our code will access the [Instagram API](https://instagram.com/developer/) to pull data. We will only use a Client ID (which will be created later) for this, so we are [limited](https://instagram.com/developer/limits/) to 5,000 requests per hour per application since we are unauthenticated.

Create an *env.sh* file inside our root directory to house the Client ID:

```sh
$ touch env.sh
```

Add this file to your *.gitignore* file since it will contain sensitive info.

## Static Files

Let's add some HTML and CSS to update the structure and style, respectively.

### HTML

Our *_base.html* will be server as the standard layout for all of our HTML pages:

***_base.html**

```html
<!DOCTYPE html>
<html>
  <head>
    <meta charset='utf-8'>
    <title>Instagram Analyzer</title>
    <!-- meta -->
    <meta name='description' content=" ">
    <meta name='author' conten=" ">
    <meta name='viewport' content="width=device-width,initial-scale=1">
    <!-- styles -->
    <link href="//maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap.min.css" rel="stylesheet" media="screen">
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

Now that we have the *_base.html* added, let's pull the base into our other HTML files.

***index.html***

```html
{% extends "_base.html" %}
{% block content %}

<h1>Python Instagram Analyzer</h1>
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

The form will display the form field for entry and a placeholder to indicate to the end user what should be entered - a hashtag, in our case. The user input will then be pulled into the Python script and used when we hit the API.

***instagram_analyzer.html***

```html
{% extends "_base.html" %}
{% block content %}

<h2>Hashtag:</h2>
<div class="well">{{ input }}</div>

<h2>Analysis:</h2>
<iframe src={{ filename }} frameborder="0" align="middle" height="600" width="650"</iframe>

<h3><a href="/">Search Again?</a></h3>

{% endblock %}
```

Here we will render the display of our analysis. The input will display the user input and the filename will display graphs that show the results of the analysis.

### CSS

Our CSS will format the contents of the page and we'll gain control of its display. Update *main.css* with:

```css
/* custom styles */

body {
  padding-top: 50px;
  padding-bottom: 20px;
}

.container {
  max-width: 700px;
  text-align: center;
}

.input {
  max-width: 200px;
}

/* Placeholder Align */

::-webkit-input-placeholder {
  text-align: center;
}

:-moz-placeholder { /* Firefox 18- */
  text-align: center;
}

::-moz-placeholder {  /* Firefox 19+ */
  text-align: center;
}

:-ms-input-placeholder {
  text-align: center;
}

/* Centering Text */
textarea {
  text-align: center;
}
input {
  text-align: center;
}
```

## Instagram API

Now that we have the HTML and CSS figured out lets take a look at the Instagram API.

### Credentials

Before any work in Python, you’ll need to first register a new client with Instagram. Once you’re logged into Instagram, you can do that [here](https://instagram.com/developer/clients/register/). An arbitrary URL and URI can be used for the sake of this exercise.

Once you’ve registered a client, you should have your own Client ID, which will be used to connect to the API. Add this to the *env.sh* file:

```sh
#!/bin/bash

export "client_id=ADD-YOUR-CLIENT-ID-HERE"
```

Let's modify the *keys.py* file to pull in our instagram API credentials:

```python
import os

CLIENT_ID = os.environ['client_id']
```

Now, when you start up your app, you can run `source env.sh` in the terminal to add the `client_id` variable to the environment.

### Configurations

*config.py* holds the app's main constants:

```python
WTF_CSRF_ENABLED = True
SECRET_KEY = "makesureyouupdateinpr0duction"
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

With that, we can now get to the code.

### Forms

The *forms.py* file validates the user input and ensures that data is entered and the length of the input is no less than 2 characters. To simplify things, we use the [Flask-WTF](https://flask-wtf.readthedocs.org/en/v0.9.5/) package:

```sh
$ pip install flask-wtf==0.9.5
$ flask freeze > requirements.txt
```

Now update *forms.py*:

```python
from flask_wtf import Form
from wtforms import TextField
from wtforms.validators import DataRequired, length


class InstagramAnalyzerForm(Form):
    keyword = TextField(
        'Keyword',
        validators=[DataRequired(), length(min=2)]
    )
```

Commit and push your code to Github and Heroku.

### Analyzer Script

The fun begins. Here, we'll be pulling utilizing *keys.py*, *config.py*, *forms.py* and all the pre-packaged Python modules to help us with-

- Pulling data from the Instagram API,
- Cleaning the data, and
- Using Pandas to display the results in a Pandas' [DataFrame](http://pandas.pydata.org/pandas-docs/version/0.16.1/generated/pandas.DataFrame.html#pandas-dataframe).

Add the following code to *instagram_analyze.py*:

```python
import requests
import datetime
import pandas as pd
from pandas.io.json import json_normalize

from keys import CLIENT_ID
from config import base_url, cols


def get(url):
    '''
    returns str(requests.get(url).json()['pagination']['next_url']
    for a specified url
    '''
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


def df_slice(df, cols):
    '''
    replaces '.' with spaces in selected column titles of a specified dataframe
    cols contained in config
    '''
    new_cols = list()
    new_df = pd.DataFrame()
    for col in cols:
        if col in df:
            new_cols.append(col)
    new_df = df[cols]
    return new_df.rename(columns=lambda x: x.replace('.', ' ').title())


def instagram_analyzer(query, n):
    '''
    returns dataframe
    iterates through and compiles a dataframe
    of n pages of instagram data from a specified url
    '''
    url = '{0}/tags/{1}/media/recent?client_id={2}&count=30'.format(
        base_url, query, CLIENT_ID)
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
    df = df.drop('index', axis=1)

    # further df cleans
    df['created_time'] = [y.replace(y, datetime.datetime.fromtimestamp(
        int(str(y))).strftime('%Y-%m-%d %H:%M:%S')) for y in df['created_time']]
    # applies df_slice to slice dataframe;
    # selects columns specified in config, cleans column titles
    df = df_slice(df, cols)

    return df
```

THIS NEEDS TO BE CLEANED UP AND BETTER EXPLAINED:
1. Our first function of the script grabs the url
1. You'll find that we're using "pagination" and "next_url" to iterate through Instagram data and pull in more than 33 posts.
1. Instagram limits us to only 33 of its most recent posts per search.
1. We do some cleaning of the data and return it in a DataFrame.
1. I'm not explicitly mentioning IPython Notebook, but know that I tested all this code in IPython Notebook before moving it over to development.

TIE THIS BACK TO THE IPYTHON NOTEBOOK. THAT'S THE POINT OF THIS POST. IPYTHON -> FLASK

Install the dependencies:

```sh
$ pip install requests==2.6.2 pandas==0.16.1
$ pip freeze > requirements.txt
```

Commit and push your code to Github and Heroku.

### Graph Script

To generate the graphs, add the following code to instagram_graphs.py*:

```python
import matplotlib.pyplot as plt


def instagram_graph(instagram_scraped):
    '''
    Displays all the graphs
    '''

    fig = plt.figure(figsize=(8, 6))

    # axis 1
    plt.subplot2grid((3, 3), (0, 0), colspan=3, rowspan=1)
    instagram_scraped['Comments Count'].plot(kind='bar', alpha=.55)
    plt.title("Total Comments Count")

    # axis 2
    plt.subplot2grid((3, 3), (1, 0), colspan=3, rowspan=1)
    instagram_scraped['Likes Count'].plot(kind='bar', alpha=.55)
    plt.title("Total Likes Count")

    # axis 3
    plt.subplot2grid((3, 3), (2, 0), colspan=3, rowspan=1)
    plt.hist(instagram_scraped['Likes Count'])
    plt.title('Distribution of Likes on Instagram Posts', fontsize=20)
    plt.xlabel('Amount of Posts', fontsize=18)
    plt.ylabel('Likes', fontsize=16)
    plt.rcParams["figure.figsize"]

    fig.tight_layout()
```

This code is designed to work with the DataFrame that gets created in *instagram_analyze.py* in order to create charts based on the analysis of data pulled from Instagram.

THIS NEEDS TO BE CLEANED UP AND BETTER EXPLAINED
TIE THIS BACK TO THE IPYTHON NOTEBOOK. THAT'S THE POINT OF THIS POST. IPYTHON -> FLASK

Don't forget to install Matplotlib:

```sh
$ pip install matplotlib==1.4.3
$ pip freeze > requirements.txt
```

Commit and push your code to Github and Heroku.

### Routes

Now, let's pull everything togther un the *\_\_init\_\_.py* file:

```python
from cStringIO import StringIO

from flask import Flask, render_template, request, \
    url_for, redirect, make_response

import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

from forms import InstagramAnalyzerForm
from instagram_analyze import instagram_analyzer
from instagram_graphs import instagram_graph


app = Flask(__name__)
app.config.from_object('instagram_analyzer_app.config')

# routes


@app.route('/', methods=['GET', 'POST'])
def main():
    form = InstagramAnalyzerForm(request.form)
    if form.validate_on_submit():
        text = form.keyword.data
        return redirect(url_for('instagram_analyze', user_input=text))
    return render_template('index.html', form=form)


@app.route("/instagram_analyze/<user_input>")
def instagram_analyze(user_input):

    return render_template(
        'instagram_analyzer.html',
        input=user_input,
        filename=user_input+".png"
    )


@app.route("/instagram_analyze/<image_name>.png")
def image(image_name):

    # Pulls in the analyzer and creates the DataFrame
    data = instagram_analyzer(image_name, 0)

    # formats the DataFrame to display plots
    instagram_graph(data)

    # renders matplotlib image to Flask view
    canvas = FigureCanvas(plt.gcf())
    output = StringIO()
    canvas.print_png(output)

    response = make_response(output.getvalue())
    response.mimetype = 'image/png'

    return response
```

The `main()` function grabs the user input from the form and then redirects the user to the `instagram_analyze/<user_input>` route where the image is formated with a ".png" extension, passed to the template, and rendered for the end user.

From there, the `image()` function is fired where we grab the data and clean it from Instagram (`data = instagram_analyzer(image_name, 0)`) and then eventually a Matplotlib graph is created.  `StringIO` us used to render the graph and display it as a png file in the template.

YOU MAY NEED TO CLEAN UP THE ROUTES

## Run it Locally

Our final step is to simply change the *run.py* to:

```python
from instagram_analyzer_app import app


if __name__ == '__main__':
    app.run(debug=True)
```

Run it locally:

```sh
$ python run.py
```

Test it out. See what happens!

ADD IMAGE

## Update Heroku

Commit your changes and then push to GitHub and Heroku.

> Keep in mind that we've added a number of dependencies since our last push, and each time you add or update dependnecies on the *requirements.txt* file, Heroku must download them. This will take some time. Be patient.

Wait! We're not done just yet. We still need to add the Instagram Client ID as an [environment/config](https://devcenter.heroku.com/articles/config-vars) variable:

```sh
$ heroku config:set client_id=ADD-YOUR-CLIENT-ID-HERE
```

This command sets the variable in the environment so that it gets picked up by the *keys.py* file.

Now check out your app in the browser:

```sh
$ heroku open
```

ADD IMAGE

## Conclusion

ADD SUMMARY!

Please add you questions/comments below. Thank you!!!