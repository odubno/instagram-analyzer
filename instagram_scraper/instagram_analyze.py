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