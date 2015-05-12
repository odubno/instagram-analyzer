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
        location = decoded['user']['location'].encode('ascii', 'ignore')
        user = decoded['user']['screen_name']
        fulltweet = decoded['text'].encode('ascii', 'ignore')
        tweetdata = '%s, @%s, %s, %s \n' % (created_at, user, fulltweet, location)
        for _ in range(100):
            try:
                saveFile = open('fightnighttweets.csv', 'a')
                if 'RT' not in tweet:
                    print tweetdata
                    saveFile.write(tweetdata)
                    saveFile.close()
                return True
            except BaseException, e:
                print 'Error:',str(e)
                time.sleep(5)
           
    def on_error(self, status):
        print status

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
twitterStream = Stream(auth, listener())
twitterStream.filter(track=keywords)
