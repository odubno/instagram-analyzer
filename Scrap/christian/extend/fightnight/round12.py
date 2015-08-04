from tweepy import Stream, OAuthHandler
from tweepy.streaming import StreamListener
import urllib
#from bs4 import BeautifulSoup as bs
import pandas as pd
import sched, time
import datetime
from creds import *
from keywords import keywords
import json

class listener(StreamListener):

    def on_data(self, data):        
        tweet = data.split(',"text":"')[1].split('","source')[0]
        decoded = json.loads(data)
        created_at = decoded['created_at']
        #location = decoded['user']['location'].encode('ascii', 'ignore') #location isn't completely necessary, and can be retrieved later on using username
        user = decoded['user']['screen_name']
        fulltweet = decoded['text'].encode('ascii', 'ignore')
        tweetdata = '%s, @%s, %s \n' % (created_at, user, fulltweet) #having fulltweet as opposed to location (which is often not provided) be the last element will make cleaning df easier
        for _ in range(1):
            try:
                saveFile = open('round12.csv', 'a')
                if 'RT' not in tweet:
                    print tweetdata
                    saveFile.write(tweetdata)
                    saveFile.close()
                return True
            except:
                time.sleep(60 * 15)
                continue
           
    def on_error(self, status):
        print status

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
twitterStream = Stream(auth, listener())
twitterStream.filter(track=['manny'])