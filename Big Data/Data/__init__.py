import time
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import os
from listener import listener
import pymongo
from pymongo import MongoClient


ckey = 'LLPdEoKpDy2eS0SH3Q51kTJLm'
consumer_secret = '3tC736rpxgLAMr7DTCapNnCUPOHhWJVp9dcdfvDSzFVmiCD95R'
access_token_key = '2917878929-jBWv0AZkEarot5z1XYLVManLBgGYAmZ8wZsMLZx'
access_token_secret = 'EOJYh4SF5n2Q8zaK059Bfb8nKV7AjILXaqjFHIxRzcqYb'
 
 
start_time = time.time() #grabs the system time
keyword_list = ['football', 'soccer'] #track list

auth = OAuthHandler(ckey, consumer_secret) #OAuth object
auth.set_access_token(access_token_key, access_token_secret)


twitterStream = Stream(auth, listener(start_time, time_limit=100000)) #initialize Stream object with a time out limit
twitterStream.filter(track=keyword_list, languages=['en'])  #call the filter method to run the Stream Object
