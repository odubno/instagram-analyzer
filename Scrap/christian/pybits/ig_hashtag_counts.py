from instagram.client import InstagramAPI
import requests
import urllib2
import json
import pandas as pd
from pandas.io.json import json_normalize
import matplotlib as mpl
from matplotlib import pyplot as plt
from glasses import *

def hashtag_summary(word):
    query = word
    hashtag_df = json_normalize(requests.get('https://api.instagram.com/v1/tags/search?q='+query+'&access_token='+acces_token).json()['data']).head()
    hashtag_df.head(5).plot(kind='barh',
		title='str 5 Tags Containing: '+query,
        y='media_count',
        x='name',
        figsize=(10,10))