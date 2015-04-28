from flask import Flask, render_template, request, flash, \
  flash, url_for, redirect

from forms import InstagramScraper

import pandas as pd
import requests
import json
from pandas.io.json import json_normalize

app = Flask(__name__)
app.config.from_object('instagram_scraper.config')


def instagram_scraper(word):

    client_id = '768fcf1f36c94eb08506bae0a9caffa3'
    secret = '54efcbaed7f64673bc93b4e28ca9e8b2'
    base_url = "https://api.instagram.com/v1"
    query=word

    url = '{0}/tags/{1}/media/recent?client_id={2}&count=5'.format(base_url, query, client_id)

    df = json_normalize(requests.get(url).json()['data'])
    
    df = df[['user.username','caption.text','tags','comments.count','likes.count',
             'filter','type','created_time','user.full_name','user.id','link','location.latitude',
             'location.longitude']]
    
    df.rename(columns={'user.username':'user_name',
                   'caption.text':'caption_text',
                   'tags':'hashtags',
                   'comments.count':'comments_count',
                   'likes.count':'likes_count',
                   'filter':'filter',
                   'created_time':'created_time',
                   'user.full_name':'full_name',
                   'user.id':'user_id',
                   'type':'type',
                   'link':'link',
                   'location.latitude':'latitude',
                   'location.longitude':'longitude'},
          inplace=True)
    
    return df



#routes 

@app.route('/', methods=['GET','POST'])
def main():
  form = InstagramScraper(request.form)
  if form.validate_on_submit():
    text = form.instagram_scrape.data
    return redirect(url_for('instagram_scrape', user_input=text))
  return render_template('index.html', form=form)


@app.route('/instagram_search/<user_input>')
def instagram_scrape(user_input):
  instagram_scraped = instagram_scraper(user_input)
  return render_template(
    'instagram_scraper.html',
    input=user_input,
    output=instagram_scraped
    )

@app.route('/about')
def home():
  return render_template('about.html')
