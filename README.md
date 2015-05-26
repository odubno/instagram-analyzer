# Instagram Scraper - from IPython to Flask  

Welcome! 

**Today we’ll take an IPython Notebook, detailing how to run analysis on images, and convert it into a Flask app that pulls images from the Instagram API, analyzes them via Pandas, and then displays charts and graphs using matplotlib.**

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

So far so good. Now lets create our app. Here's structure for our app:
```
├── run.py
└── requirements.txt
```