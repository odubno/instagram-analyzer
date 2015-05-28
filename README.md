# Instagram Scraper - from IPython to Flask  

Welcome! 

**Today we’ll take an IPython Notebook, detailing how to run analysis using Instagram data, and convert it into a Flask app that pulls data from the Instagram API, analyze the data via Pandas, and then display charts and graphs using matplotlib.**

>IPython Notebook is my personal favorite for constucting scripts and getting quick analysis on data. But how do you get your graphs and findings onto the web for others to use?

In the first two parts, we'll begin by first structuring our working environment and in the 3rd part we'll work on pulling in our back-end logic that I personally always run in IPython Notebook.

1. *Part One*: Setup the local development environment along with the basic Flask app.
1. *Part Two*: Setup the production environment on Heroku and push the current application to the cloud.
1. *Part Three*: Add in the back-end logic to access the Instagram API, process the data with Pandas/Numpy, and create the charts with matplotlib for analysis.

Having focused solely on data science, we're excited to present how to take an IPython Notebook, containing all of our data work, and strip out the relevant parts to build out the Flask back-end and then add a nice front-end so that our work can be displayed in a browser for the world to see.

> Keep in mind that this is a low-level tutorial for those looking to get familiar with Flask, understand the development workflow, and deploy a basic app to Heroku.

Enjoy!

## Part One: Local Development

Let's quickly setup a basic environment for local development utilizing the following tools - [virtualenv](http://www.virtualenv.org/en/latest/), [Flask](http://flask.pocoo.org/), and [Heroku](https://heroku.com)

Make a new directory, create/activate a virtualenv, and initialize a Git repo:

```
sh
$ mkdir instagram_scraper
$ cd instagram_scraper
```


Create the virtual env:
```sh
$ pip install virtualenv
$ virtualenv --no-site-packages venv
$ source venv/bin/activate
```


> **Remember**: The virtualenv allows us to neutralize our environment and work exclusively with the tools necessary for our app.

Install Flask and create the *requirements.txt* file, which will become important later when Heroku looks to install the necessary libraries when we deploy to production:

```
sh
$ pip install Flask
$ pip freeze
$ touch requirements.txt
$ pip freeze > requirements.txt
```

Finally, add a remote Git repo on Github and commit your changes before pushing your current code up to Github. It's  a good practice frequently to add/commit your code locally and push your changes to GitHub. 

First click "New Repository" inside you GitHub account, create a name and click "Create Repository". Copy/Paste the code you get from GitHub into your shell and click Enter:

```
echo "# instagram_scraper" >> README.md
git init
git add README.md
git commit -m "first commit"
git remote add origin https://github.com/<username>/instagram_scraper.git
git push -u origin master
```

> You just initialized your repo within your directory with a README.md file and pushed your changes up to github. 


So far so good. Now lets create our app. Here's the current structure of our app (for now):
```
├── README.md
├── run.py
└── requirements.txt
```
Create "run.py":
```sh
$ touch run.py
```

Open up run.py in your favorite editor and add the following code:

```
from flask import Flask
app = Flask(__name__)


@app.route('/')
def main():
    return "Python Instagram Scraper"

if __name__ == '__main__':
    app.run()
```

Run the app locally:

```$ python run.py```

You should see the displayed text of "Python Instagram Scraper" in action on http://localhost:5000/. Kill the server.

Let's get Heroku up and running. 

## Part Two: Setup Heroku

Given you have the Heroku [Toolbelt](https://toolbelt.heroku.com/) installed, follow the steps below to get the app up and running. See [link](https://devcenter.heroku.com/articles/getting-started-with-python#introduction) for more info on using Python with Heroku.

Lets create a Procfile and add the following code:

```$ touch Procfile```

Add this code to the Procfile:

```$ web: gunicorn run:app```

> Basically, you name one process perline you want to run on heroku, currently we just want to run our app.

Make sure to add gunicorn to requirements.txt:

```
$ pip install gunicorn
$ pip freeze > requirements.txt
```

Lets create our app and initialize it:

```
$ heroku create instagram-scraper
$ git init
```

Let's add heroku servers as a remote for heroku git repositories, so we're able to call "git push heroku" and push our code to heroku: 

```$ heroku git:remote -a instagram-scraper```

Commiting and pushing our code up to Heroku:

```
$ git add .
$ git commit -m "first commit"
$ git push heroku master
```

Your terminal should display a link similar to https://instagram-scraper.herokuapp.com/. Follow it and you should see our app.

Here's a [video](https://www.youtube.com/watch?v=pmRT8QQLIqk) that I found super helpful in deploying my app to Heroku.

Current structure of our app:
```
├── README.md
├── run.py
├── Procfile
└── requirements.txt
```
## Part Three: Back-End Logic 

Lets create new folders and python files inside our directory. Follow the structure of our app below:

```
sh
$ touch .gitignore
$ mkdir instagram_scraper_app
$ cd instagram_scraper_app
$ touch __init__.py instagram_analyze.py instagram_graphs.py key.py forms.py config.py
$ mkdir templates
$ cd templates 
$ touch instagram_scraper.html index.html _base.html
$ cd ..
$ mkdir static
$ cd static
$ mkdir css js
$ cd css
$ touch bootstrap.min.css main.css
$ cd ..
```

Structure of the app:
```
instagram_scraper
|
├── instagram_scraper_app
|   |
|   ├── static
|   |   |
|   |   └── css
|   |       ├── bootstrap.min.css
|   |       └── main.css
|	|
|	├── templates
|	|	├── _base.html
|	|	├── index.html
|	|	└── instagram_scraper.html
|	|
|	├── __init__.py
|	├── config.py
|	├── forms.py
|	├── instagram_analyze.py
|	├── instagram_graphs.py
|	├── keys.py
|	└── run.py
|	
├── README.md
├── .gitignore
├── run.py
├── Procfile
└── requirements.txt
```

We'll work on creating our instagram scraper. Our code will iterate through instagram using for loops and instagram pagination to pull in more data. Instagram is capped at 33 posts per hit and 5,000 posts that you could pull within 24 hours. 

There's some code cleaning and imports from config.py and forms.py

config.py simply holds variables for our url and data features we're interested in pulling. 

forms.py is our form validator for when the user searches their specific hashtag. 


## Part Three-A: Setting Up .gitignore

The file ".gitignore" gets picked up by GitHub and hides folders/files that you don't want others to see. Add these files to .gitignore:

```
venv
*.pyc
*.db
keys.py
```
## Part Three-B: Templates, HTML and CSS

Click [here](https://raw.githubusercontent.com/odubno/instagram_scraper/master/instagram_scraper_app/static/css/bootstrap.min.css) and copy/paste this css code into bootstrap.min.css

Click [here](https://raw.githubusercontent.com/odubno/instagram_scraper/master/instagram_scraper_app/static/css/main.css) and copy paste this code into main.css

Our css will format the contents of the page and we'll gain control of its display. 

Our _base.html will be the standard layout for all of our HTML pages. As opposed to typing out our css for each HTML page we could simply pull it in from our base:

_base.html
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

Configure the index.html. This form will display a form field for entry and a placeholder to indicate what should be entered. In our case a hashtag.

index.html
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

instagram_scraper.html will render the display of our analysis. The input will be what the user had entered and the filename will be our graphs

instagram_scraper.html
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


