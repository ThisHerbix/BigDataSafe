import time
from tweepy.streaming import StreamListener
from pymongo import MongoClient
import json


class listener(StreamListener):

    def __init__(self, start_time, time_limit= 100000):

        self.time = start_time
        self.limit = time_limit
    
    def on_data(self, data):
        while (time.time() - self.time) < self.limit:
            try:
                client = MongoClient('localhost', 27017)
                db = client['twitter_db']
                collection = db['twitter_collection']
                tweet = json.loads(data)
                collection.insert(tweet)
                #print collection
                
                #saveFile = open('raw_tweets.json', 'a')
                #saveFile.write(data)
                #saveFile.write('\n')
                #saveFile.close()
                print data
               

                return True


            except BaseException, e:
                print 'failed ondata,', str(e)
                time.sleep(5)
                pass

        exit()
        
    def on_error(self, status):

        print status
        
  
