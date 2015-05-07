from config import *
from forms import InstagramScraper
import requests
import json
from pandas.io.json import json_normalize
from keys import *
import pandas as pd

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
<<<<<<< HEAD
    for _ in range(1): #range should ideally be determined by the user; 2 replaced by n, n defined in the same place word is defined.
=======
    
    for _ in range(n):
>>>>>>> 4526052d8135d50b699eae32ad76bdd57651f0bf
        x = get(url) 
        urls.append(str(x)) 
        url = get(x) 
            
    for url in urls:
<<<<<<< HEAD
        results.append(json_normalize(requests.get(url).json()['data']))
    df = pd.DataFrame().append(results).reset_index().drop('index',axis=1)

    # except:
    #     errors.append(
    #         "Error: Make sure that the search is just the word string, without spaces or hashtag signs." # <<< was getting error earlier, turned out to be an import error, not a string error.
    #         )
    #     return errors
    #     print sys.exc_info()[0] #<<< handling exceptions will need to be expanded later on
	
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

    return df



    #return likes_count, str("people like"), total_posts, str("recent posts containing #"+word+"!"), str(float(comments_count)/float(likes_count)
     #   )[:5]+'% of Instagram users who have liked posts containing #'+word,'have commented on a post.'


=======
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
    df = df_slice(df, cols) #applies df_slice to slice dataframe
    return df.head()
>>>>>>> 4526052d8135d50b699eae32ad76bdd57651f0bf
