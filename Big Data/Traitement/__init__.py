from pymongo import MongoClient
import pymongo
from pymongo.collection import Collection
import re


#Cette fonction retourne le nombre de fois qu'un mot du sac de mot a ete rencontre.
def TwtWhichContainOneWord(collection, searchedWord):
    nombreOccurence = collection.find({"text" : {'$regex' : '.*' + searchedWord +'.*'}}).count()
    return nombreOccurence


#Cette fonction retourne la somme du nombre de tweet contenant les mots du sac de mot donnes en parametre auront ete rencontre.
#ATTENTION Ce nombre peut donc depasser le nombre de tweet contenu dans la base !
def TwtWhichContainOneWordOfABagOfWord(collection, *bagOfSearchedWord):
    nombreOccurence = 0
    for i in range(len(bagOfSearchedWord)):
        word = bagOfSearchedWord[i]
        nombreOccurence  = nombreOccurence + collection.find({"text" : {'$regex' : '.*' + word +'.*'}}).count()
    return nombreOccurence

#Cette fonction retourne le nombre de tweet contenant un sac de mot complet.
#ATTENTION le nombre de mot est limite a 5
def twtWhichContainABagOfWord(collection, *bagofword):
    wordList = ['','','','','']
    for i in range(len(bagofword)):
        wordList[i] = bagofword[i]
    nombreOccurence = collection.find({'$and':[{'text' : {'$regex' : '.*' + wordList[0] +'.*'}}
                                               ,{'text' : {'$regex' : '.*' + wordList[1] +'.*'}}
                                               ,{'text' : {'$regex' : '.*' + wordList[2] +'.*'}}
                                               ,{'text' : {'$regex' : '.*' + wordList[3] +'.*'}}
                                               ,{'text' : {'$regex' : '.*' + wordList[4] +'.*'}}]}).count()
    return nombreOccurence

client = MongoClient('localhost', 27017)
db = client['twitter_db']
collection = db['twitter_collection']

bagofword = ['football', 't', 'r','e', 'z']


a = TwtWhichContainOneWord(collection,'ok')
print "Nb tweets contenant ok = "+str(a) 
a = TwtWhichContainOneWord(collection,'football')
print "Nb tweets contenant football = "+str(a) 
a = TwtWhichContainOneWordOfABagOfWord(collection, *bagofword)
print "Nb tweets contenant l'un des mots du sac de mot = "+str(a) 
a = twtWhichContainABagOfWord(collection, *bagofword)
print 'Nb MAIN tweet contenant tous les mots du sac = '+str(a)

