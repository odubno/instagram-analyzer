# Instagram Scraper - from IPython to Flask  

Welcome! 

**Today we’ll take an IPython Notebook, detailing how to run analysis using instagram data, and convert it into a Flask app that pulls data from the Instagram API, analyzes the data via Pandas, and then displays charts and graphs using matplotlib.**

>IPython Notebook is my personal favorite for constucting scripts and getting quick analysis on data. But how do you get your script onto the web?

In the first two parts, we'll begin by first structuring our working environment and in the 3rd part we'll work on pulling in our back end logic that I personally always run in IPython Notebook.

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

Lets create a new folder and python files inside our directory. Follow the structure of our app below:

```
sh
$ mkdir instagram_scraper_app
$ cd instagram_scraper_app
$ touch __init__.py instagram_analyze.py instagram_graphs.py key.py forms.py config.py
$ mkdir templates
$ cd templates 
$ touch instagram_scraper.html index.html
$ cd ..
```

Structure of the app:
```
instagram_scraper
|
├── instagram_scraper_app
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
├── run.py
├── Procfile
└── requirements.txt

```

We'll work on creating our instagram scraper. Our code will iterate through instagram using for loops and instagram pagination to pull in more data. Instagram is capped at 33 posts per hit and 5,000 posts that you could pull within 24 hours. 

There's some code cleaning and imports from config.py and forms.py

config.py simply holds variables for our url and data features we're interested in pulling. 

forms.py is our form validator for when the user searches their specific hashtag. 

Lets create our code for instagram_analyze.py:

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

Code for config.py:

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

Code for forms.py:

```
from flask_wtf import Form
from wtforms import TextField
from wtforms.validators import DataRequired, length 

class InstagramScraper(Form):
  instagram_scrape = TextField(
    'Scrape', validators=[DataRequired(), length(min=2)])
```

