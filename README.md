# Instagram Analyzer - from IPython to Flask

Welcome!

**Today we’ll take an IPython Notebook that pulls data from Instagram, analyzes the data via Pandas and converts the IPython Notebook into a Flask app that will display charts and graphs using Matplotlib.**

![Alt text](/static/img/instagram_analyze_page.jpg "Landing Page")

*This is a guest post by Oleh Dubno with help from Christian Tirol.*

*Oleh is a beginner Python Developer from New York City. He's currently contracting as a Web Crawling Developer at <a href="https://www.quovo.com/splash/index.php" target="_blank">Quovo</a>, a fintech startup. He began his quest, moving from Accounting to picking up Data Science, in August of 2014. Since then he has finished courses using Python at General Assembly, Thinkful, Coursera, CodeSchool and Udacity. See some of his other projects <a href="http://www.olehdubno.com/" target="_blank">here</a>. He currently has weekly mentoring sessions with Michael Herman, a RealPython mentor.*

*Christian is ...*

### A. Instagram Analyzer in IPython Notebook

In the first part, before development, you'll see the gradual progression of using IPython Notebook to get data from Instagram, clean the data and visualize everything using Matplotlib:

IPython Notebook Files:

• [Using the Instagram Client ID to get the data and pull everything into a pandas DataFrame](https://github.com/odubno/instagram_scraper/blob/master/IPython_Notebook_Files/01_instagram_analyze_json_DataFrame.ipynb)

• [Creating a function using the code form the previous notebook and cleaning Instagram Data](https://github.com/odubno/instagram_scraper/blob/master/IPython_Notebook_Files/02_instagram_analyze_Data_Cleaning.ipynb)

• [Developing our function and visualizing Instagram data using Matplotlib](https://github.com/odubno/instagram_scraper/blob/master/IPython_Notebook_Files/03_instagram_analyze_Matplotlib.ipynb)


> The code from the IPython Notebook links above will be copied into a text editor during the tutorial and will be used in deploying our app. Viewing the above links is recommended if you'd like to see the code move from the notebook to development. 

### B. Instagram Analyzer in Development

In the first two parts of deploying our app, we'll begin by structuring the working environment and in the third part we'll work on porting the back-end logic from the [IPython Notebook files](https://github.com/odubno/instagram_scraper/tree/master/IPython_Notebook_Files) to the Flask application:

1. *Part One*: Setup the local development environment along with the basic Flask app.
1. *Part Two*: Setup the production environment on Heroku and push the current application to the cloud.
1. *Part Three*: Add in the back-end logic to access the Instagram API, process the data with Pandas/Numpy, and create the charts with matplotlib.

We're excited to present how to take an IPython Notebook, containing all of our data work, and strip out the relevant parts to build out the Flask back-end and then add a nice front-end so that our work can be displayed in a browser for the world to see.

> Keep in mind that this is a low-level tutorial for those looking to get familiar with Flask, understand the development workflow, convert code from IPython Notebook to development, and deploy a basic app to Heroku.

Enjoy!

#### Dependencies for the app:

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
$ git remote add origin https://github.com/YourAccount/instagram_analyzer.git
$ git push -u origin master
```

Now add a *.gitignore* using the command:

```
$ touch .gitignore
```
And hide certain files and folders from the public in the .gitignore:

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
├── requirements.txt
├── run.py
└── venv
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

You should see the displayed text of "Python Instagram Analyzer" in action at [http://localhost:5000/](http://localhost:5000/). Once done, kill the server. *CTRL+C*

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

To rename the app:
```
$ heroku apps:rename newname
```
[Link](https://devcenter.heroku.com/articles/renaming-apps#updating-git-remotes) explaining how to rename your app in heroku.

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

Current files in inside *.gitignore*:
```
.DS_Store
*.pyc
venv
```

After adding your file:
```
.DS_Store
*.pyc
venv
env.sh
```

## Static Files

Let's add some HTML and CSS to update the structure and style, respectively.

### HTML

Our *_base.html* will serve as the standard layout for all of our HTML pages:

***_base.html***

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

The form will display the form field for entry and a placeholder to indicate to the end user what to enter - a hashtag, in our case. The user input will then enter the hashtag. Then the Python script that we will pull in from our IPython Notebook will be used to pull the data from Instagram and run the analysis.

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

Let's modify the *keys.py* file, located inside **instagram_analyzer_app** folder, to pull in our Instagram client_id credentials:

```python
import os

CLIENT_ID = os.environ['client_id']
```
  
>> This is to keep your Keys hidden during deployment.

Now, when you start up your app, you can run `source env.sh` in the terminal to add the `client_id` variable to the environment.

###Instagram Analyze Script

Here we're pulling in the back-end logic that we worked on in the [first](https://github.com/odubno/instagram_scraper/blob/master/IPython_Notebook_Files/01_instagram_analyze_json_DataFrame.ipynb) and the [second](https://github.com/odubno/instagram_scraper/blob/master/IPython_Notebook_Files/02_instagram_analyze_Data_Cleaning.ipynb) IPython Notebook. 

The script below uses the Instagram client_id to pull in the 30 most recent Instagram posts into a Pandas DataFrame and cleans up the columns and rows to display it back in a DataFrame. 

Follow the comments in the script for an indepth understanding.

In the script below, we'll be importing json_normalize. Here's a [medium article](https://medium.com/@amirziai/flattening-json-objects-in-python-f5343c794b10) that explains how json_normalize works.

```
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

Here's a side by side comaparison of the IPython Notebook script to what we have above. 

![Alt text](/static/img/instagram_anayze_1.jpg "Instagram Analyze IPython Notebook code camparison")


