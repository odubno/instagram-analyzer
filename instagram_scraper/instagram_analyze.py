from forms import InstagramScraper
import requests
import json
from pandas.io.json import json_normalize
from glasses import *



def instagram_scraper(word):

    base_url = "https://api.instagram.com/v1"
    query=word
    errors = []
    
    try:
        url = '{0}/tags/{1}/media/recent?client_id={2}&count=20'.format(base_url, query, client_id)
        df = json_normalize(requests.get(url).json()['data'])
    except:
        errors.append(
            "Error: Make sure that the search is just the word string, without spaces or hashtag signs."
            )
        return errors
    
    # Cleaning up the Data Frame
    df = df[['user.username','caption.text','tags','comments.count','likes.count',
             'filter','type','created_time','user.full_name','user.id','link','location.latitude',
             'location.longitude']]
    
    # Changing the column names in the Data Frame
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

    total_posts = len(df)
    comments_count = df['comments_count'].sum()
    likes_count = df['likes_count'].sum()

    return likes_count, "people like", total_posts, "recent posts containing #"+word+"!"
    return str(float(comments_count)/float(likes_count)
        )[:5]+'% of Instagram users who have liked psots containing #'+word,'have commented on a post.'


