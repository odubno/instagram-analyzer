#is it possible to save 'url' 
from forms import InstagramScraper
import requests
import json
import pandas as pd
from pandas.io.json import json_normalize
from glasses import *

def get_urls(url, n):

      #return a next_url
    def get(url):
        return str(requests.get(url).json()['pagination']['next_url'])
    
      #open list to hold urls
    urls = list() 
    
      #handling initial url
    urls.append(str(url)) #add initial url to list

      #handling further urls    
    for _ in range(n):
        x = get(url) 
        urls.append(str(x)) #add next_url
        url = get(x) #replaces initial url with next_url for next turn in loop

      #open list to hold data
    results = list()

      #populate df with data from urls in urls
    for url in urls:
        results.append(json_normalize(requests.get(url).json()['data']))

      #initiate df
    df = pd.DataFrame().append(results).reset_index().drop('index',axis=1)