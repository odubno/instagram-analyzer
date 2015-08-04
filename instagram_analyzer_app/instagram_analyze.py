import requests
from pandas.io.json import json_normalize
import pandas as pd
import datetime

from keys import CLIENT_ID

def instagram_analyzer(query):
    base_url = "https://api.instagram.com/v1"
    url = '{0}/tags/{1}/media/recent?client_id={2}&count=30'.format(
        base_url, query, CLIENT_ID)
    r = requests.get(url)
    j = r.json()  
    results = []
    if 'data' in j: 
        data = j['data']
        df_instance = json_normalize(data)
        results.append(df_instance)
        
    df = pd.DataFrame().append(results)

    df['created_time'] = [
    y.replace(y, datetime.datetime.fromtimestamp(int(str(y))).strftime(
    '%Y-%m-%d %H:%M:%S')) for y in df['created_time']]
    cols = [
        'user.username',
        'caption.text',
        'tags',
        'comments.count',
        'likes.count',
        'filter',
        'type',
        'created_time',
        'user.full_name',
        'user.id',
        'link',
        'location.latitude',
        'location.longitude'
    ]   
    df_cols = df[cols]
    df_clean = df_cols.rename(columns=lambda x: x.replace('.',' ').title())

    return df_clean