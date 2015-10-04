# Instagram Analyzer - from IPython to Flask

Welcome!

**Today we’ll detail how to convert an IPython Notebook - which pulls data from Instagram and analyzes the data via Pandas - into a Flask web application.**

ADD IMAGE

*This is a guest post by Oleh Dubno with help from Christian Tirol. <a href="mailto:olehdubno@gmail.com">Oleh</a> is a Python Developer from New York City, currently working at <a href="https://www.quovo.com/splash/index.php" target="_blank">Quovo</a>, a fintech startup. <a href="mailto:tirol.christian@gmail.com">Christian</a> is an Analyst working in New York City with the Analytics and Reporting Infrastructure teams at <a href="http://www.adroitdigital.com/">Adroit Digital<a/>, a MediaMath subsidiary.*

## Getting Started

### Instagram Analyzer in IPython Notebook

Before diving into Flask, let's look at the gradual progression of using IPython Notebook to grab data from Instagram, clean the data in Pandas and then visualize everything using Matplotlib.

**IPython Notebook Files**:

- [Using the Instagram Client ID to get the data and pull everything into a pandas DataFrame](https://github.com/odubno/instagram_analyzer/blob/master/IPython_Notebook_Files/01_instagram_analyze_json_DataFrame.ipynb)
- [Creating a function using the code form the previous notebook and cleaning Instagram Data](https://github.com/odubno/instagram_analyzer/blob/master/IPython_Notebook_Files/02_instagram_analyze_Data_Cleaning.ipynb)
- [Developing our function and visualizing Instagram data using Matplotlib](https://github.com/odubno/instagram_analyzer/blob/master/IPython_Notebook_Files/03_instagram_analyze_Matplotlib.ipynb)

### Instagram Analyzer in Development, an overview

In the first two parts of deploying our app, we'll begin by structuring the working environment, both locally and in the cloud, and in the third part we'll work on porting the back-end logic from the [IPython Notebook files](https://github.com/odubno/instagram_analyzer/tree/master/IPython_Notebook_Files) to the Flask application:


### TODO  RL posts for setting up local environment. 
1. *Part One*: Setup the local development environment along with the basic Flask app.
1. *Part Two*: Setup the production environment on Heroku and push the current application to the cloud.
1. *Part Three*: Add in the back-end logic to access the Instagram API, process the data with Pandas/Numpy, and create the charts with matplotlib.

We're excited to present how to take an IPython Notebook, containing all of the data work, and strip out the relevant parts to build out the Flask back-end and then add a nice front-end so that the work can be displayed in a browser for the world to see.

> Keep in mind that this is a low-level tutorial for those looking to get familiar with Flask, understand the development workflow, convert code from IPython Notebook to development, and deploy a basic app to Heroku.

Enjoy!

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

Let's quickly setup a basic environment for local development utilizing the following tools - [virtualenv](http://www.virtualenv.org/en/latest/), [Flask](http://flask.pocoo.org/), and [Heroku](https://heroku.com).

Create a project directory and create/activate a virtualenv:

```sh
$ mkdir instagram_analyzer && cd instagram_analyzer
$ virtualenv venv
$ source venv/bin/activate
```

> **Remember**: The virtualenv allows us to neutralize our environment and work exclusively with the tools necessary for our app.

Install Flask and create the *requirements.txt* file, which will become important later when Heroku deploying to Heroku:

``` sh
$ pip install Flask==0.10.1
$ pip freeze > requirements.txt
```

Add a local Git repo along with a basic *README.md* file:

```sh
$ git init
$ echo "# Instagram Analyzer" >> README.md
```

Now add a *.gitignore*:

```sh
$ touch .gitignore
```

And add the following files and folders:

```
.DS_Store
*.pyc
venv
```

> It's good practice to add system files (like *.DS_Store), dependency folers (like "venv"), and any sensitive information (more on this later) to the *.gitignore* file.

Then add a remote Git repo on Github and commit your changes locally before pushing your current code up to Github.

So far so good. Now lets create our basic project structure.

```sh
$ touch run.py
```

Your project directory should now look like this:


```sh
├── README.md
├── requirements.txt
├── run.py
└── venv
```

Open *run.py* in your favorite editor (like [Sublime Text 3](https://realpython.com/blog/python/setting-up-sublime-text-3-for-full-stack-python-development/)) and add the following code:

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

You should see the displayed text of "Python Instagram Analyzer" in action at [http://localhost:5000/](http://localhost:5000/). Kill the server when done.

Now let's get Heroku up and running!

## Heroku Setup

Given you have the Heroku [Toolbelt](https://toolbelt.heroku.com/) installed, follow the steps below to get the app up and running. *For more info on using Python with Heroku, check out the official [Heroku documenation](https://devcenter.heroku.com/articles/getting-started-with-python#introduction)*.

Create a Procfile and add the following code:

```sh
$ echo "web: gunicorn run:app" >> Procfile
```

Basically, you name one process/service per line that you want to run on Heroku in the Procfile; currently we just want to run our app.

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

Checkout your app in action!

```sh
$ heroku open
```

## More Structure

Lets beef up the structure!

```sh
$ mkdir instagram_analyzer_app && cd instagram_analyzer_app
$ touch __init__.py instagram_analyze.py instagram_graphs.py keys.py forms.py
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

Next, we'll work on creating our Instagram analyzer within *instagram_analyze.py*. to access the [Instagram API](https://instagram.com/developer/) to pull relevant data. We will only use a Client ID (which will be created later) for this, so we are [limited](https://instagram.com/developer/limits/) to 5,000 requests per hour.

Create an *env.sh* file inside our root directory to house the Client ID:

```sh
$ touch env.sh
```

Add this file to your *.gitignore* file since it will contain sensitive info.

## Instagram, Pandas, and Matplotlib

Here we'll be pulling in the code from the IPython Notebook files

### Credentials

Before any work in Python, you’ll need to first register a new client with Instagram. Once you’re logged into Instagram, you can do that [here](https://instagram.com/developer/clients/register/). An arbitrary URL and URI can be used for the sake of this exercise.

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

Now, when you start up your app, you can run `source env.sh` in the terminal to add the `client_id` variable to the environment.

### Instagram Analyze Script

Here we're pulling in the back-end logic that we worked on in the [first](https://github.com/odubno/instagram_analyzer/blob/master/IPython_Notebook_Files/01_instagram_analyze_json_DataFrame.ipynb) and the [second](https://github.com/odubno/instagram_analyzer/blob/master/IPython_Notebook_Files/02_instagram_analyze_Data_Cleaning.ipynb) IPython Notebook.

The script below uses the Instagram client_id to pull in the 30 most recent Instagram posts into a Pandas DataFrame and cleans up the columns and rows to display it back in a DataFrame.

Follow the comments in the script for an indepth understanding.

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

from keys import CLIENT_ID

def instagram_data(query):
    base_url = "https://api.instagram.com/v1"
    url = '{0}/tags/{1}/media/recent?client_id={2}&count=30'.format(
        base_url, query, CLIENT_ID)

    page = requests.get(url)
    page_json = page.json()

    # The format of our json are 3 different dictionaries: *pagination*, *meta* and *data*. We're interested in *data*.

    # *data* is a list of nested dictionaries. What json_normalize will do is flatten everything and create columns for nested dictionary titles.

    results = []
    if 'data' in page_json:
        data = page_json['data']
        df_instance = json_normalize(data)
        results.append(df_instance)

    df = pd.DataFrame().append(results)

  # Our dates are a bit messy. Let's clean it up

    df['created_time'] = [
    y.replace(y, datetime.datetime.fromtimestamp(int(str(y))).strftime(
    '%Y-%m-%d %H:%M:%S')) for y in df['created_time']]

  # These are the columns that we personally took interest in.
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

  # Minor ocd cleaning before returning our data set.
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
app.config.update(
    WTF_CSRF_ENABLED =
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


Try it out:

![Alt text](/instagram_analyzer_app/static/img/instagram_analyze_page.jpg "Landing Page")

Things to always keep in mind:
> Always run source env.sh before running the app.
> Remember to push your code up to github and then to heroku for deployment.
