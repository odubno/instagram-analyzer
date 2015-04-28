from forms import InstagramScraper
import requests
import json
from pandas.io.json import json_normalize
from glasses import *
import matplotlib


def instagram_scraper(word):

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


