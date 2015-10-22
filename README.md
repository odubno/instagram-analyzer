# Instagram Analyzer - from IPython to Flask

Welcome!

**This post details how to convert an IPython Notebook into a Flask web application.** More specifically, we'll take an IPython Notebook, containing all of the data work, strip out the relevant parts to build out the Flask back-end, and then add a nice front-end so that the work can be displayed in a browser for the world to see.

ADD IMAGE

*This is a guest post by Oleh Dubno with help from Christian Tirol. <a href="mailto:olehdubno@gmail.com">Oleh</a> is a Python Developer from NYC, currently working at <a href="https://www.quovo.com/splash/index.php" target="_blank">Quovo</a>, a fintech startup. <a href="mailto:tirol.christian@gmail.com">Christian</a> is an Analyst working in New York City with the Analytics and Reporting Infrastructure teams at <a href="http://www.adroitdigital.com/">Adroit Digital<a/>.*

## Getting Started

### Instagram Analyzer in IPython Notebook

Before diving into Flask, let's look at the gradual progression of using IPython Notebook to grab data from Instagram, clean the data in Pandas, and then visualize everything using Matplotlib.

**IPython Notebook Files**:

- [Grab the data from Instragram](https://github.com/odubno/instagram_analyzer/blob/master/IPython_Notebook_Files/01_instagram_analyze_json_DataFrame.ipynb)
- [Clean the Instagram Data](https://github.com/odubno/instagram_analyzer/blob/master/IPython_Notebook_Files/02_instagram_analyze_Data_Cleaning.ipynb)
- [Visualize the Instagram data via Matplotlib](https://github.com/odubno/instagram_analyzer/blob/master/IPython_Notebook_Files/03_instagram_analyze_Matplotlib.ipynb)

### Instagram Analyzer in Development - An Overview

In the first two parts of deploying our app, we'll begin by structuring the working environment, both locally and in the cloud, and in the third part we'll work on porting the back-end logic from the [IPython Notebook files](https://github.com/odubno/instagram_analyzer/tree/master/IPython_Notebook_Files) to the Flask application:

1. *Part One*: Set up the local development environment along with the basic Flask app.
1. *Part Two*: Set up the production environment on Heroku and push the current application to the cloud.
1. *Part Three*: Add in the back-end logic to access the Instagram API, process the data with Pandas/Numpy, and create the charts with Matplotlib.

*Make sure to grab the boilerplate structure from the [Github repo](ADD LINK).*

### Dependencies for the app:

```sh
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

We'll also be using the latest version of Python 2.

## Structure

```sh
├── Procfile
├── README.md
├── instagram_analyzer_app
│   ├── __init__.py
│   ├── forms.py
│   ├── instagram_analyze.py
│   ├── instagram_graphs.py
│   ├── keys.py
│   ├── static
│   │   ├── css
│   │   │   └── main.css
│   │   └── js
│   └── templates
│       ├── _base.html
│       ├── index.html
│       └── instagram_analyzer.html
├── requirements.txt
└── run.py
```

Let's quickly setup a basic environment for local development utilizing the following tools and services - [virtualenv](http://www.virtualenv.org/en/latest/), [Flask](http://flask.pocoo.org/), and [Heroku](https://heroku.com).

## Heroku Setup

Heroku setup in not necessary, but nice if you'd like to showcase your app on the web.

Check [Heroku Setup](https://github.com/odubno/instagram_analyzer/blob/master/heroku_setup.md) to integrate it with your app.


## Instagram, Pandas, and Matplotlib

Here we'll be pulling in the code from the IPython Notebook files

### Credentials

Before any work in Python, you’ll need to first register a new application with Instagram. Once you’re logged into Instagram, you can do that [here](https://instagram.com/developer/clients/register/). An arbitrary URL and URI can be used for the sake of this exercise.

Once you’ve registered a client, you should have your own Client ID, which will be used to connect to the API. Add this to the *env.sh* file, like so:

```sh
#!/bin/bash

export "client_id=ADD-YOUR-CLIENT-ID-HERE"
```

Let's modify the *keys.py* file, located inside "instagram_analyzer_app" folder, to pull in our Instagram client_id credentials:

```python
import os

CLIENT_ID = os.environ['client_id']
```

> For environ to work make sure to run `source env.sh` in the terminal to add the `client_id` variable to the environment.

### Instagram Analyze Script

Here we're pulling in the back-end logic from IPython Notebook [first](https://github.com/odubno/instagram_analyzer/blob/master/IPython_Notebook_Files/01_instagram_analyze_json_DataFrame.ipynb) and the [second](https://github.com/odubno/instagram_analyzer/blob/master/IPython_Notebook_Files/02_instagram_analyze_Data_Cleaning.ipynb) IPython Notebook.

The script below uses the Instagram client_id to pull in the 30 most recent Instagram posts into a Pandas DataFrame and clean the columns and rows up to display our data.

Follow the comments in the script for a better understanding.

Install the necessary modules:

```sh
$ pip install requests==2.6.2 pandas==0.16.1 matplotlib==1.4.3
$ pip freeze > requirements.txt
```

Add the following code to *instagram_analyze.py*:

```python
import requests
from pandas.io.json import json_normalize
import pandas as pd
import datetime

from keys import CLIENT_ID

def instagram_analyzer(query):
    base_url = "https://api.instagram.com/v1"
    url = '{0}/tags/{1}/media/recent?client_id={2}&count=30'.format(
        base_url, query, CLIENT_ID)
    r = requests.get(url)
    j = r.json()
    results = []
    if 'data' in j:
        data = j['data']
        df_instance = json_normalize(data)
        results.append(df_instance)

    df = pd.DataFrame().append(results)

    cols = [
        'comments.count',
        'likes.count',
    ]
    df_cols = df[cols]
    df_clean = df_cols.rename(columns=lambda x: x.replace('.',' ').title())

    return df_clean
```

Here's a side by side comparison of The IPython Notebook script (on the left) and the above script ready for deployment (on the right).

![Alt text](/instagram_analyzer_app/static/img/instagram_anayze_1.jpg "Instagram Analyze IPython Notebook code camparison")

### Matplotlib Script

Before moving forward with integrating our *instagram_analyze.py* script with Flask lets modify our *instagram_graphs.py* to display graphs. We'll be returning to the [third](https://github.com/odubno/instagram_analyzer/blob/master/IPython_Notebook_Files/03_instagram_analyze_Matplotlib.ipynb) IPython Notebook to pull in the code that displays our graphs using Matplotlib.

Add the code below to *instagram_graphs.py*:

```python
import matplotlib.pyplot as plt

def instagram_graph(instagram_analyzed):

    fig = plt.figure(figsize=(8, 6))

  # Using subplots for multiple graphs
    plt.subplot2grid((3, 3), (0, 0), colspan=3, rowspan=1)
    instagram_analyzed['Comments Count'].plot(kind='bar', alpha=.55)
    plt.title("Total Comment Count Per Post", fontsize=20)
    plt.ylabel('Total Comments')
    plt.xlabel('Most Recent to Least Recent')

    plt.subplot2grid((3, 3), (1, 0), colspan=3, rowspan=1)
    instagram_analyzed['Likes Count'].plot(kind='bar', alpha=.55)
    plt.title("Total Like Count Per Post", fontsize=20)
    plt.xlabel('Most Recent to Least Recent')
    plt.ylabel('Total Likes')

    plt.subplot2grid((3, 3), (2, 0), colspan=3, rowspan=1)
    plt.hist(instagram_analyzed['Likes Count'])
    plt.title('Test Graph (Please Ignore)', fontsize=20)
    plt.xlabel('Amount of Posts')
    plt.ylabel('Likes')
    plt.rcParams["figure.figsize"]

    fig.tight_layout()
```
### Routes (*\_\_init\_\_.py* and *run.py*)

Update *run.py*:

```python
from instagram_analyzer_app import app

if __name__ == '__main__':
    # port = int(os.environ.get('PORT', 5000))
    app.run(debug=True)
```

> *\_\_init\_\_.py* creates our directories and executes our back-end logic, while *run.py* returns our app.

Inside the "instagram_analyzer_app" open up your *\_\_init\_\_.py file and add:

```python
from cStringIO import StringIO
from flask import Flask, render_template, request, \
  flash, url_for, redirect, make_response, send_file
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import matplotlib.pyplot as plt


from instagram_analyze import instagram_analyzer
from instagram_graphs import instagram_graph
from forms import InstagramAnalyzer


app = Flask(__name__)

# For form protection. Note that the SECRET_KEY could litterally be any string you'd like.
# If this is production then do make the key impossible to guess.
app.config.update(
    WTF_CSRF_ENABLED = True
    ,SECRET_KEY = "pass"
    )

# ROUTES

@app.route('/', methods=['GET', 'POST'])
def main():
    form = InstagramAnalyzer(request.form)
    if form.validate_on_submit():
        text = form.instagram_analyze.data
        return redirect(url_for('instagram_analyze', user_input=text))
    return render_template('index.html', form=form)


@app.route("/instagram_analyze/<user_input>")  # 1
def instagram_analyze(user_input):

    return render_template(
        'instagram_analyzer.html',
        input=user_input,
        filename=user_input+".png"  # 2
    )

"""
The beginning of the route @app.route("/instagram_analyze/<user_input>") picks
up what the user had passed as a search. ".png" is then appended to user_input to create
the image title.

The ending of the url will show up as the input and reference the filename.
Both routes have "/instagram_analyze/..." this causes the response route to render
the user_input with the ".png" ending
@app.route("/instagram_analyze/<image_name>.png")
"""

@app.route("/instagram_analyze/<image_name>.png")  # 3
def image(image_name):
    # pulls in the scraper and creates the DataFrame
    instagram_analyzed = instagram_analyzer(image_name)

    # formats the DataFrame to display plots
    instagram_graph(instagram_analyzed)

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

Now to the front-end...

## HTML

In order to avoid repeating our HTML structure, we'll create a *\_base.py* that will extend and employ template inheritance:

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

Now let's create an *index.html* file, which extends from the base template:

```html
{% extends "_base.html" %}
{% block content %}

<h1>Python Instagram Analyzer</h1>

<br>

<center>
  <form class="input" role="form" method="post" action="">
    {{ form.csrf_token }}
    <p>
      {{ form.instagram_analyze(class="form-control input-lg", placeholder="Enter Hashtag")}}
      <span class="error">
        {% if form.instagram_analyze.errors %}
          {% for error in form.instagram_analyze.errors %}
            {{ error }}
          {% endfor %}
        {% endif %}
      </span>
    </p>
    <button class="btn btn-default btn-lg" type="submit">Analyze!</button>
  </form>

  <br>

  <p>Click <a href="/about">here</a> to read about the app.</p>

</center>

{% endblock %}
```

Within the *instagram_analyzer.html* file, whatever the user passes on the submit form will be rendered as the filename. Refer to the structure of *\_\_init\_\_.py* and see this in action. We'll be displaying our matplotlib graphs inside an iframe and sourcing the filename as explained above.

```html
{% extends "_base.html" %}

{% block content %}

<center>
  <h2>Hashtag:</h2>
  <div class="well input">{{ input }}</div>
  <h2>Analysis:</h2>
  <iframe src={{ filename }} frameborder="0" align="middle" height="600" width="800"></iframe>
  <h3><a href="/"> Search Again?</a></h3>
</center>

{% endblock %}
```

## Conclusion

We learned how to use Python to pull in the most recent Instagram posts in IPython Notebook and deploy our results on Heroku.

Modifications moving forward may include pulling in more than 30 most recent posts at a time, improving our HTML/CSS layout and upgrading the information revealed in the Matplotlib graphs.


Try it out: <a href="http://instagram-analyzer.herokuapp.com/">Instagram-Analyzer</a>

<a href="http://instagram-analyzer.herokuapp.com/"><img src="/instagram_analyzer_app/static/img/instagram_analyze_page.jpg" alt="Instagram Analyzer"></a>

Things to always keep in mind:
> Always run source env.sh before running the app.
> Remember to push your code up to github and then to heroku for deployment.
