## Heroku Setup

> create an .md file for how to setup heroku and reference it here.

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

Next, we'll work on creating our Instagram analyzer within *instagram_analyze.py*. to access the [Instagram API](https://instagram.com/developer/) to pull relevant data. We will only use a Client ID (which will be created later) for this, so we are [limited](https://instagram.com/developer/limits/) to 5,000 requests per hour.

Create an *env.sh* file inside our root directory to house the Client ID:

```sh
$ touch env.sh
```

Add this file to your *.gitignore* file since it will contain sensitive info.
