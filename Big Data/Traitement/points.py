# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
from pymongo import MongoClient

MONGO_DATABASE_NAME = 'twitter_db3'
MONGO_COLLECTION_NAME = 'twitter_collection3'
client = MongoClient('localhost', 27017)
db = client[MONGO_DATABASE_NAME ]
collection = db[MONGO_COLLECTION_NAME]

ABS_CENTER = 0                                        #Valeur de départ en abscisse
ORD_CENTER = 0                                    #Valeur de départ en ordonnée

#Fonction qui calcule une patie de la distance(meaning _similarity) en se basant sur la concordance des Hashtags
def defineTwtHashTagDistanceValue():
    hashtaglist = []
    hashtagValue = []
    for tweets in collection.find():
        hashtaglist.append(tweets['hashtag'])
        identi = tweets['_id']
        collection.update({'_id': identi},{'$set': {'meaning_similarity': ABS_CENTER}})
        hashtagValue.append(tweets['meaning_similarity'])
    for index in range(len(hashtaglist)):
        if(index+1 <len(hashtaglist)):
            hashtagsactuel = hashtaglist[index]
            hashtagssuivant =  hashtaglist[index+1]
            for hashtag1 in hashtagsactuel:
                for hashtag2 in hashtagssuivant:
                    if(hashtag1 == hashtag2):
                        hashtagValue[index] = hashtagValue[index]-20
    for index, tweets in enumerate(collection.find()):
        identi = tweets['_id']
        collection.update({'_id': identi},{'$set': {'meaning_similarity': hashtagValue[index]}})     
    return hashtagValue
#Fonction qui calcule une partie de la distance(meaning_similarity) en se basant sur la concordance de mot
def defineTwtWordsDistanceValue():
    wordslist = []
    wordValue = []
    for tweets in collection.find():
        wordslist.append(tweets['words'])
        identi = tweets['_id']
        wordValue.append(tweets['meaning_similarity'])
        
    for index in range(len(wordslist)):
        if(index+1 <len(wordslist)):
            hashtagsactuel = wordslist[index]
            hashtagssuivant =  wordslist[index+1]
            for hashtag1 in hashtagsactuel:
                for hashtag2 in hashtagssuivant:
                    if(hashtag1 == hashtag2):
                        wordValue[index] = wordValue[index]-20
                    if(hashtag1 != hashtag2):
                        wordValue[index] = wordValue[index]+20
    for index, tweets in enumerate(collection.find()):
        identi = tweets['_id']
        collection.update({'_id': identi},{'$set': {'meaning_similarity': wordValue[index]}})
    return wordValue

#Fonction qui calcule une partie de la distance(other_similarity) en se basant sur la distance
def defineGeoTwtDistance():
    geolist = []
    geoValue = []
    for tweets in collection.find():
        identi = tweets['_id']
        if(tweets['geo'] == None):
            collection.update({'_id': identi},{'$set': {'geo': 'missing'}})
        geoValue.append(tweets['other_similarity'])
        geolist.append(tweets['geo'])
        
    for index in range(len(geolist)):
        if(index+1 <len(geolist)):
            geoactuel = geolist[index]
            geosuivant =  geolist[index+1]
            if(geoactuel != 'missing'):
                if(geosuivant != 'missing'):
                    if(geoactuel == geosuivant):
                        geoValue[index] = geoValue[index]-20
                    else:
                        geoValue[index] = geoValue[index]+20
    for index, tweets in enumerate(collection.find()):
        identi = tweets['_id']
        collection.update({'_id': identi},{'$set': {'other_similarity': geoValue[index]}})
    return geoValue
#Fonction qui change la distance entre deux points en se basant sur la lang
def defineLangTwtDistance():
    langlist = []
    langValue = []
    for tweets in collection.find():
        identi = tweets['_id']
        if(tweets['lang'] == None):
            collection.update({'_id': identi},{'$set': {'lang': 'missing'}})
        langValue.append(tweets['other_similarity'])
        langlist.append(tweets['lang'])
        
    for index in range(len(langlist)):
        if(index+1 <len(langlist)):
            langactuel = langlist[index]
            langsuivant =  langlist[index+1]
            if(langactuel != 'missing'):
                if(langsuivant != 'missing'):
                    if(langactuel == langsuivant):
                            langValue[index] = langValue[index]-20
                    if(langactuel != langsuivant):
                            langValue[index] = langValue[index]+20
    for index, tweets in enumerate(collection.find()):
        identi = tweets['_id']
        collection.update({'_id': identi},{'$set': {'other_similarity': langValue[index]}})
    return langValue

def defineUser_activityTwtDistance():
    user_activitylist = []
    user_activityValue = []
    for tweets in collection.find():
        identi = tweets['_id']
        user_activityValue.append(tweets['other_similarity'])
        user_activitylist.append(tweets['user_activity'])
        
    for index in range(len(user_activitylist)):
        if(index+1 <len(user_activitylist)):
            user_actuel = user_activitylist[index]
            if(user_actuel <= 3):
                user_activityValue[index] = user_activityValue[index]+5
            if(user_actuel >= 5 and user_actuel <= 15):
                user_activityValue[index] = user_activityValue[index]+10
            if(user_actuel >=15 and user_actuel <= 30):
                user_activityValue[index] = user_activityValue[index]+20
            if(user_actuel >=15 and user_actuel <= 30):
                user_activityValue[index] = user_activityValue[index]+50
    for index, tweets in enumerate(collection.find()):
        identi = tweets['_id']
        collection.update({'_id': identi},{'$set': {'other_similarity': user_activityValue[index]}})
    print user_activityValue
    return user_activityValue

#Fonction qui met les valeurs de similarité à leur valeur de base
def setSimilarity(collection):
    for tweets in collection.find():
        identi = tweets['_id']
        collection.update({'_id': identi},{'$set': {'meaning_similarity': ABS_CENTER}})
        collection.update({'_id': identi},{'$set': {'other_similarity': ORD_CENTER}})

#Fonction qui permet de convertir une donné depuis mongoDB en list        
def dataMeaningtoList(collection, typeofmeaning):
    meaninglist = []
    for tweets in collection.find():
        meaninglist.append(tweets[typeofmeaning])
    return meaninglist

#Fonction qui remet les valeurs de similarité à leur valeur de départ (0) et qui recalcule les similarités 
def TestSimilarity(collection):
    setSimilarity(collection)
    defineTwtHashTagDistanceValue()
    defineTwtWordsDistanceValue()
    defineGeoTwtDistance()
    defineLangTwtDistance()
    defineUser_activityTwtDistance()

TestSimilarity(collection)

plt.title('Nuage de points avec Matplotlib')
plt.xlabel('sens')
plt.ylabel('autres')
x = []
y = []
x = dataMeaningtoList(collection, 'meaning_similarity')
y = dataMeaningtoList(collection, 'other_similarity')

del x[-1]
del y[-1]
plt.scatter(x,  y)
print x
print y
plt.savefig('ScatterPlot.png')
plt.show()