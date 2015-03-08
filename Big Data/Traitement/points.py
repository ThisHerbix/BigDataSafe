import matplotlib.pyplot as plt
from pymongo import MongoClient

MONGO_DATABASE_NAME = 'twitter_db3'
MONGO_COLLECTION_NAME = 'twitter_collection3'
client = MongoClient('localhost', 27017)
db = client[MONGO_DATABASE_NAME ]
collection = db[MONGO_COLLECTION_NAME]

ABS_CENTER = 100
ORD_CENTER = 200

x = [ 5.1,  4.9,  4.7,  4.6,  5.,   5.4,  4.6,  5.,   4.4,  4.9,  5.4,  4.8,  4.8,  4.3,  5.8,
      5.7,  5.4,  5.1,  5.7,  5.1,  5.4,  5.1,  4.6,  5.1,  4.8,  5.,   5.,   5.2,  5.2,  4.7,
      4.8,  5.4,  5.2,  5.5,  4.9,  5.,   5.5,  4.9,  4.4,  5.1,  5.,   4.5,  4.4,  5.,   5.1,
      4.8,  5.1,  4.6,  5.3,  5.,   7.,   6.4,  6.9,  5.5,  6.5,  5.7,  6.3,  4.9,  6.6,  5.2,
      5.,   5.9,  6.,   6.1,  5.6,  6.7,  5.6,  5.8,  6.2,  5.6,  5.9,  6.1,  6.3,  6.1,  6.4,
      6.6,  6.8,  6.7,  6.,   5.7,  5.5,  5.5,  5.8,  6.,   5.4,  6.,   6.7,  6.3,  5.6,  5.5,
      5.5,  6.1,  5.8,  5.,   5.6,  5.7,  5.7,  6.2,  5.1,  5.7,  6.3,  5.8,  7.1,  6.3,  6.5,
      7.6,  4.9,  7.3,  6.7,  7.2,  6.5,  6.4,  6.8,  5.7,  5.8,  6.4,  6.5,  7.7,  7.7,  6.,
      6.9,  5.6,  7.7,  6.3,  6.7,  7.2,  6.2,  6.1,  6.4,  7.2,  7.4,  7.9,  6.4,  6.3,  6.1,
      7.7,  6.3,  6.4,  6.,   6.9,  6.7,  6.9,  5.8,  6.8,  6.7,  6.7,  6.3,  6.5,  6.2,  5.9 ]

y = [ 3.5,  3.,   3.2,  3.1,  3.6,  3.9,  3.4,  3.4,  2.9,  3.1,  3.7,  3.4,  3.,   3.,   4.,
      4.4,  3.9,  3.5,  3.8,  3.8,  3.4,  3.7,  3.6,  3.3,  3.4,  3.,   3.4,  3.5,  3.4,  3.2,
      3.1,  3.4,  4.1,  4.2,  3.1,  3.2,  3.5,  3.1,  3.,   3.4,  3.5,  2.3,  3.2,  3.5,  3.8,
      3.,   3.8,  3.2,  3.7,  3.3,  3.2,  3.2,  3.1,  2.3,  2.8,  2.8,  3.3,  2.4,  2.9,  2.7,
      2.,   3.,   2.2,  2.9,  2.9,  3.1,  3.,   2.7,  2.2,  2.5,  3.2,  2.8,  2.5,  2.8,  2.9,
      3.,   2.8,  3.,   2.9,  2.6,  2.4,  2.4,  2.7,  2.7,  3.,   3.4,  3.1,  2.3,  3.,   2.5,
      2.6,  3.,   2.6,  2.3,  2.7,  3.,   2.9,  2.9,  2.5,  2.8,  3.3,  2.7,  3.,   2.9,  3.,
      3.,   2.5,  2.9,  2.5,  3.6,  3.2,  2.7,  3.,   2.5,  2.8,  3.2,  3.,   3.8,  2.6,  2.2,
      3.2,  2.8,  2.8,  2.7,  3.3,  3.2,  2.8,  3.,   2.8,  3.,   2.8,  3.8,  2.8,  2.8,  2.6,
      3.,   3.4,  3.1,  3.,   3.1,  3.1,  3.1,  2.7,  3.2,  3.3,  3.,   2.5,  3.,   3.4,  3. ]

def defineTwtHashTagDistanceValue():
    hashtaglist = []
    hashtagValue = []
    for tweets in collection.find():
        hashtaglist.append(tweets['hashtag'])
        identi = tweets['_id']
        collection.update({'_id': identi},{'$set': {'meaning_similarity': ABS_CENTER}})
    for index in range(len(hashtaglist)):
        hashtagValue.append(ABS_CENTER)
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

def defineTwtWordsDistanceValue():
    wordslist = []
    wordValue = []
    for tweets in collection.find():
        wordslist.append(tweets['words'])
        identi = tweets['_id']
        collection.update({'_id': identi},{'$set': {'other_similarity': ORD_CENTER}})
        
    for index in range(len(wordslist)):
        wordValue.append(ORD_CENTER)
        if(index+1 <len(wordslist)):
            hashtagsactuel = wordslist[index]
            hashtagssuivant =  wordslist[index+1]
            for hashtag1 in hashtagsactuel:
                for hashtag2 in hashtagssuivant:
                    if(hashtag1 == hashtag2):
                                wordValue[index] = wordValue[index]-20
    for index, tweets in enumerate(collection.find()):
        identi = tweets['_id']
        collection.update({'_id': identi},{'$set': {'other_similarity': wordValue[index]}})
                                
    return wordValue
        
def giveHashtagValue(hashtaglist1, hashtaglist2):
    for hashtag1 in hashtaglist1:
        for hashtag2 in hashtaglist2:
            if hashtag2.find(hashtag1):
                print 'ok'

def dataMeaningtoList(collection, typeofmeaning):
    meaninglist = []
    for tweets in collection.find():
        meaninglist.append(tweets[typeofmeaning])
    return meaninglist


defineTwtHashTagDistanceValue()
defineTwtWordsDistanceValue()

plt.title('Nuage de points avec Matplotlib')
plt.xlabel('sens')
plt.ylabel('autres')

plt.scatter(dataMeaningtoList(collection, 'meaning_similarity'),dataMeaningtoList(collection, 'other_similarity'))
plt.savefig('ScatterPlot.png')
plt.show()





