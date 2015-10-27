# Instagram Analyzer - from IPython to Flask

Welcome!

**This post details how to convert an IPython Notebook into a Flask web application.** More specifically, we'll take an IPython Notebook, containing all of the data work, strip out the relevant parts to build out the Flask back-end, and then add a nice front-end so that the world can see your work.

ADD IMAGE

*This is a guest post by Oleh Dubno with help from Christian Tirol. <a href="mailto:olehdubno@gmail.com">Oleh</a> is a Python Developer from NYC, currently working at <a href="https://www.quovo.com/splash/index.php" target="_blank">Quovo</a>, a fintech startup. <a href="mailto:tirol.christian@gmail.com">Christian</a> is an Analyst working in New York City with the Analytics and Reporting Infrastructure teams at <a href="http://www.adroitdigital.com/">Adroit Digital<a/>.*

## Workflow

Before diving into Flask, take a look at, and interact with, the IPython Notebooks:

- [Extract data from Instagram](https://github.com/odubno/instagram_analyzer/blob/master/IPython_Notebook_Files/01_instagram_analyze_json_DataFrame.ipynb)
- [Clean the data](https://github.com/odubno/instagram_analyzer/blob/master/IPython_Notebook_Files/02_instagram_analyze_Data_Cleaning.ipynb)
- [Visualize the data via Matplotlib](https://github.com/odubno/instagram_analyzer/blob/master/IPython_Notebook_Files/03_instagram_analyze_Matplotlib.ipynb)

Make sure you understand the code in this Notebooks as they set the basis for the Flask app. Now, we can being the conversion process, from IPython to Flask:

1. *Part One*: Set up the local development environment along with the basic Flask app.
1. *Part Two*: Add in the back-end logic to access the Instagram API, process the data with Pandas/Numpy, and create the charts with Matplotlib.

## Part One - Getting Started

Grab the boilerplate from the Github [repo](https://github.com/realpython/instagram-analyzer):

```sh
$ git clone git@github.com:realpython/instagram-analyzer.git
$ cd instagram-analyzer
$ git checkout tags/v1
```

Check out the [dependencies](https://github.com/realpython/instagram-analyzer/blob/master/requirements.txt) and Python version as well as the project structure:

```sh
├── _config.py
├── app
│   ├── __init__.py
│   ├── forms.py
│   ├── instagram_analyze.py
│   ├── instagram_graphs.py
│   ├── static
│   │   ├── css
│   │   │   └── main.css
│   │   └── js
│   └── templates
│       ├── _base.html
│       ├── analysis.html
│       └── index.html
├── requirements.txt
└── run.py
```

Activate your [virtualenv](http://www.virtualenv.org/en/latest/) and install the dependencies:

```sh
$ virtualenv env
$ source env/bin/activate
$ pip install -r requirements.txt
```

Test this out before moving on to the second part:

```sh
$ python run.py
```

Navigate in your browser to [localhost:5000](localhost:5000), and you should see "Hello World!". Now, let's convert our IPython scripts over to the Flask app!

## Part Two - IPython to Flask

Here we'll be pulling in the code from the IPython Notebook files, iteratively...

### Instagram Registration

Before any work in Python, you’ll need to first register a new application with Instagram. First, sign up for Instagram (if necessary), and then log in. Once you’re logged in, you can set up an app from the [Developer Portal](https://instagram.com/developer/clients/register/). An arbitrary URL and URI can be used for the sake of this exercise.

Once you’ve registered a client, you should have your own Client ID, which will be used to connect to the API. Add this to the *_config.py* file, like so:

```python
INSTAGRAM_CLIENT_ID = '0755d115c19d38939d357b33fe8138bc'
```

Finally, move the config file into "app" directory.

### Data Extraction and Analysis

Within the *instagram_analyze.py* script, we will add the back-end logic from the first two IPython Notebooks - [data extraction](https://github.com/odubno/instagram_analyzer/blob/master/IPython_Notebook_Files/01_instagram_analyze_json_DataFrame.ipynb) and [data cleansing](https://github.com/odubno/instagram_analyzer/blob/master/IPython_Notebook_Files/02_instagram_analyze_Data_Cleaning.ipynb).

Start by installing the necessary packages:

```sh
$ pip install requests==2.6.2 pandas==0.16.1 matplotlib==1.4.3
$ pip freeze > requirements.txt
```

Now add the following code to *instagram_analyze.py*:

```python
import requests
from pandas.io.json import json_normalize
import pandas as pd

from _config import INSTAGRAM_CLIENT_ID


def instagram_analyzer(query):
    base_url = "https://api.instagram.com/v1"
    url = '{0}/tags/{1}/media/recent?client_id={2}&count=30'.format(
        base_url, query, INSTAGRAM_CLIENT_ID)
    request = requests.get(url)
    json_results = request.json()
    results = []
    if 'data' in json_results:
        data = json_results['data']
        df_instance = json_normalize(data)
        results.append(df_instance)

    df = pd.DataFrame().append(results)

    cols = [
        'comments.count',
        'likes.count',
    ]
    df_cols = df[cols]
    df_clean = df_cols.rename(columns=lambda x: x.replace('.', ' ').title())

    return df_clean
```

Here we make a call to the Instagram API to pull in the thirty most recent Instagram posts. The posts are then added to a Pandas DataFrame and cleaned to better display the data.

Want to test this script? Add the following code to the bottom-

```python
print(instagram_analyzer('javascript'))
```

-and then run the script-

```sh
$ python app/instagram_analyze.py
```

You should see something like:

```sh
Comments Count  Likes Count
0                1            8
1                0            7
2                0          116
3                1            8
4                0           11
5                0            8
6                0            6
7                0           11
8                0           16
9                0           28
10               0           15
11               0           20
12               0           40
13               1           21
14               5           15
15               1           43
16               0           12
17               3           48
18               3           24
19               3           66
20               5           76
21               4           40
22               2           19
23               1           33
24               0           30
25               1           26
26               1           46
27               1           26
28               7          158
29               2           20
```

Image comparing notebook to the script

<a><img src="/instagram_analyzer_app/static/img/script_vs_notebook_1.jpg" alt="Instagram Analyzer"></a>

### Data Visualization

Next, let's integrate the [third](https://github.com/odubno/instagram_analyzer/blob/master/IPython_Notebook_Files/03_instagram_analyze_Matplotlib.ipynb) IPython Notebook into our app, which utilizes Matplotlib to create charts and graphs.

Add the following code to *instagram_graphs.py*:

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

### Routes

Update  *\_\_init\_\_.py* like so:

```python
from cStringIO import StringIO
from flask import Flask, render_template, request, url_for, redirect, \
    make_response
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import matplotlib.pyplot as plt

from instagram_analyze import instagram_analyzer
from instagram_graphs import instagram_graph
from forms import InstagramAnalyzer


app = Flask(__name__)
app.config.update(
    WTF_CSRF_ENABLED=True,
    SECRET_KEY='my precious'
)


# routes

@app.route('/', methods=['GET', 'POST'])
def main():
    form = InstagramAnalyzer(request.form)
    if form.validate_on_submit():
        text = form.instagram_analyze.data
        return redirect(url_for('instagram_analyze', user_input=text))
    return render_template('index.html', form=form)


@app.route("/instagram_analyze/<user_input>")
def instagram_analyze(user_input):
    return render_template(
        'analysis.html',
        input=user_input,
        filename=user_input+".png"  # create image title based on user input
    )


@app.route("/instagram_analyze/<image_name>.png")
def image(image_name):

    # create the DataFrame
    instagram_analyzed = instagram_analyzer(image_name)

    # format the DataFrame to display plots
    instagram_graph(instagram_analyzed)

    # render matplotlib image to Flask view
    canvas = FigureCanvas(plt.gcf())
    output = StringIO()
    canvas.print_png(output)

    # create response
    response = make_response(output.getvalue())
    response.mimetype = 'image/png'

    return response
```

Make sure to read through the inline comments in this script to better understand what's happening. With that, let's jump to the front-end...

### HTML

ADD INFO ABOUT JINJA, LINK TO REAL PYTHON BLOG POST

In order to avoid repeating common parts of the HTML structure, we'll create a *\_base.py* that employs [template inheritance](https://realpython.com/blog/python/primer-on-jinja-templating/#template-inheritance):

```html
<!DOCTYPE html>
<html>
  <head>
    <meta charset='utf-8'>
    <title>Instagram Analyzer</title>
    <!-- styles -->
    <link href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap.min.css" rel="stylesheet">
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

<h1 class="text-center">Python Instagram Analyzer</h1>

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

</center>

{% endblock %}
```

Within the *analysis.html* file, the text that the end user submits in the form will be rendered as the image filename. Refer back to *\_\_init\_\_.py* to see this in action. We'll be displaying our matplotlib graphs inside an iframe and sourcing the filename as explained above.

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

### Forms

BRIEFLY EXPLAIN WHAT's HAPPENING HERE

```python
from flask_wtf import Form
from wtforms import TextField
from wtforms.validators import DataRequired, length


class InstagramAnalyzer(Form):
    instagram_analyze = TextField(
        'Analyze', validators=[DataRequired(), length(min=2)])
```

## Test

DETAIL HOW TO RUN THE APP

## Conclusion

1. WHAT DID WE LEARN?
1. WHAT ELSE CAN WE DO? Modifications moving forward may include pulling in more than 30 most recent posts at a time, improving our HTML/CSS layout and upgrading the information revealed in the Matplotlib graphs.


Try it out: <a href="http://instagram-analyzer.herokuapp.com/">Instagram-Analyzer</a>

<a href="http://instagram-analyzer.herokuapp.com/"><img src="/instagram_analyzer_app/static/img/instagram_analyze_page.jpg" alt="Instagram Analyzer"></a>

Cheers!
