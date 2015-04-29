#print Where does your hashtag stand on Instagram?

from instagram.client import InstagramAPI
import requests
import urllib2
import json
import pandas as pd
from pandas.io.json import json_normalize
import matplotlib as mpl
from matplotlib import pyplot as plt

#later on, import token separately so token can be updated as necessary in a separate file
token = '1265541089.d4ec778.3a455b41bc6643cbb2e0c406cfcce3ff'

query = raw_input('Enter a hashtag you would like to search: ')
df = json_normalize(requests.get('https://api.instagram.com/v1/tags/search?q='+query+'&access_token='+token).json()['data']).head()

df.head(5).plot(kind='barh',
		title='str 5 Tags Containing: '+query,
        y='media_count',
        x='name',
        figsize=(10,10))
		
#currently, plots will not show.
#save for later