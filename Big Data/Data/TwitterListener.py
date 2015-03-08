# -*- coding: utf-8 -*-
import tweepy
import json
from pymongo import MongoClient
from tweepy import OAuthHandler
from tweepy import Stream
import re
import time

MONGO_DATABASE_NAME = 'twitter_db3'
MONGO_COLLECTION_NAME = 'twitter_collection3'

consumer_key = 'LLPdEoKpDy2eS0SH3Q51kTJLm'
consumer_secret = '3tC736rpxgLAMr7DTCapNnCUPOHhWJVp9dcdfvDSzFVmiCD95R'
access_token = '2917878929-jBWv0AZkEarot5z1XYLVManLBgGYAmZ8wZsMLZx'
access_token_secret = 'EOJYh4SF5n2Q8zaK059Bfb8nKV7AjILXaqjFHIxRzcqYb'

#Fonction remplaçant les caracteres non-alphanumerique par des espaces
def replaceAll(text):
    #ajouter dans removelist les caracteres a conserver
    removelist = "=# " 
    text = re.sub(r'[^\w'+removelist+']','',text)
    return text
#Fonction permettant de supprimer les informations inutiles au projet
def removeUselessData(data):
    
    if data.has_key('contributors'):
        del data['contributors']
    if data.has_key('truncated'):
        del data['truncated']
    if data.has_key('in_reply_to_status_id'):
        del data['in_reply_to_status_id']
    if data.has_key('source'):
        del data['source']
    if data.has_key('timestamp_ms'):    
        del data['timestamp_ms']
    if data.has_key('in_reply_to_screen_name'):
        del data['in_reply_to_screen_name']
    if data.has_key('entities'):
        del data['entities']
    if data.has_key('id_str'):           
        del data['id_str']
    if data.has_key('in_reply_to_user_id'):
        del data['in_reply_to_user_id'] 
    if data.has_key('user'):                 
        del data['user']
    if data.has_key('in_reply_to_user_id_str'):
        del data['in_reply_to_user_id_str']
    if data.has_key('possibly_sensitive'):
        del data['possibly_sensitive']
    if data.has_key('in_reply_to_status_id_str'):
        del data['in_reply_to_status_id_str']
    if data.has_key('retweeted_status'):
        del data['retweeted_status']
    if data.has_key('extended_entities'):
        del data['extended_entities']
    if data.has_key('place'):
        del data['place']
    if data.has_key('filter_level'):
        del data['filter_level']
             
    return data

class TwitterListener(tweepy.StreamListener):
    
    
    def __init__(self, start_time, time_limit= 100000):

        self.time = start_time
        self.limit = time_limit
    
    def on_data(self, data):
        while (time.time() - self.time) < self.limit:
            try:
                #Connection à mongoDb
                client = MongoClient('localhost', 27017)
                db = client[MONGO_DATABASE_NAME ]
                collection = db[MONGO_COLLECTION_NAME]
                #Récupération d'un tweet en JSON    
                tweet = json.loads(data)
                #Suppression des informations inutiles
                tweet = removeUselessData(tweet)
                #Transformation du tweet dans un format plus simple à traiter
                
                if(tweet.has_key('lang')):
                        lang = tweet['lang']
                        if(tweet.has_key('text')):
                            text = tweet['text']
                            
                            if(lang == 'en'):
                                text.encode('ascii', 'ignore')
                                #print "TEXT = "+text
                                #On remplaçe les caracteres non-alphanumerique par des espaces
                                text = replaceAll(text)
                                wordlist = text.split()
                                #On met tous les mots en minuscule
                                wordlist = [wordlist[word].lower() for word in range(len(wordlist))]
                                #On supprime les mots de moins de 3 lettres
                                wordlist = [word for word in wordlist if len(word) > 3]
                                #On enlève les URL que les utilisateurs on pu mettre                        
                                wordlist = [word for word in wordlist if (word.find('http')) == -1]
                                #On reforme le tweet pour le stocker dans MongoDB
                                identi = tweet['id']
                                text = ' '.join(wordlist)
                                a = OneTwtDictionnary(text)
                                words = getOneTwtWords(a)
                                occurences = getOneTwtOccurrences(a)
                                hashtags = getHashtag(words, occurences)
                                
                                tweet['text'] = text
                                tweet['words'] = words
                                tweet['nbwords'] = occurences
                                tweet['hashtag'] = hashtags
                                user_activity = collection.find({'id' : identi}).count()+1
                                tweet['user_activity'] = user_activity
                                tweet['meaning_similarity'] = -1
                                tweet['other_similarity'] = -1
                                collection.insert(tweet)
                               
                                    
                                print tweet
                return True
            
            except BaseException, e:
                print 'failed ondata,', str(e)
                time.sleep(5)
                pass
        exit()
    

    def on_error(self, status):
        print status

start_time = time.time()

def start_stream():
    while True:
        try:
            #Authentification auprès de twitter
            auth = OAuthHandler(consumer_key, consumer_secret)
            auth.set_access_token(access_token, access_token_secret)

            #Obtention du flux
            twitterStream = Stream(auth, TwitterListener(start_time, time_limit=100000))
            twitterStream.filter(track=["android"])
        except:
            continue
        
def OneTwtDictionnary(twt):
    dictionnary = {}
    words = twt.split()
    for word in range(len(words)):
        if dictionnary.has_key(words[word]):
            value = dictionnary[words[word]]
            dictionnary[words[word]] = value+1
        else: 
            dictionnary[words[word]] = 1               
    return dictionnary

def getHashtag(words, occurences):
    hashtaglist = []
    i = len(words)-1
    while(i >=0):
        if("#" in words[i]):
            hashtaglist.append(words[i])
            del occurences[i]
            del words[i]
        i = i-1 
    return hashtaglist
    
def getOneTwtWords(dictionnary):
    return dictionnary.keys()

def getOneTwtOccurrences(dictionnary):
    return dictionnary.values()

start_stream()

        
        