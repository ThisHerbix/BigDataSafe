from pymongo import MongoClient
import pymongo
from pymongo.collection import Collection
import re
from reportlab.graphics.barcode.eanbc import words
import pickle

MONGO_DATABASE_NAME = 'twitter_db2'
MONGO_COLLECTION_NAME = 'twitter_collection2'

#Cette fonction retourne le nombre de fois qu'un mot du sac de mot a ete rencontre.
def TwtWhichContainOneWord(collection, searchedWord):
    nombreOccurence = collection.find({"text" : {'$regex' : '.*' + searchedWord +'.*'}}).count()
    return nombreOccurence


#Cette fonction retourne la somme du nombre de tweet contenant les mots du sac de mot donne en parametre auront ete rencontre.
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

def retrieveTwt(collection):
    for obj in collection.find({'text':{'$exists' : True}}):
        if obj:
            text = obj['text']
            print text
def LoadDictionnary(collection):
    dictionnary = dict()
    dictionnary = {}
    for obj in collection.find({'text':{'$exists' : True}}):
        if obj:
            text = obj['text']
            words = re.split(r'[,; _\/\\]*',text)
            for word in range(len(words)):
                if dictionnary.has_key(words[word]):
                    value = dictionnary[words[word]]
                    dictionnary[words[word]] = value+1
                else: 
                    dictionnary[words[word]] = 1   
    return dictionnary

def OneTwtDictionnary(twt, dictionnary):
    dictionnary = dict()
    dictionnary = {}
    words = twt.split()
    for word in range(len(words)):
        if dictionnary.has_key(words[word]):
            value = dictionnary[words[word]]
            dictionnary[words[word]] = value+1
        else: 
            dictionnary[words[word]] = 1               
    return dictionnary
def maxList(list):
    return max(list)
 
def mostSaidWords(Occurencelist, wordlist, Nbmots):

    print Occurencelist.index(max(Occurencelist))
    print wordlist[Occurencelist.index(max(Occurencelist))]
    print max(Occurencelist)
    for i in range(1,Nbmots):
        print i
        indexOccurMax = Occurencelist.index(max(Occurencelist))
        del Occurencelist[indexOccurMax]
        del wordlist[indexOccurMax]
        #print Occurencelist.index(max(Occurencelist))
        print max(Occurencelist)
        print wordlist[Occurencelist.index(max(Occurencelist))]

client = MongoClient('localhost', 27017)
db = client[MONGO_DATABASE_NAME ]
collection = db[MONGO_COLLECTION_NAME]

bagofword = ['football', 't', 'r','e', 'z']


#a = TwtWhichContainOneWord(collection,'ok')
#print "Nb tweets contenant ok = "+str(a) 
#a = TwtWhichContainOneWord(collection,'football')
#print "Nb tweets contenant football = "+str(a) 
#a = TwtWhichContainOneWordOfABagOfWord(collection, *bagofword)
#print "Nb tweets contenant l'un des mots du sac de mot = "+str(a) 
#a = twtWhichContainABagOfWord(collection, *bagofword)
#print 'Nb tweet contenant tous les mots du sac = '+str(a)
#retrieveTwt(collection)

a = dict()
#a = OneTwtDictionnary('ok ok ok prout find test find test dans ta geule geule geule', a)
a = LoadDictionnary(collection)
output = open('/home/alexis/Bureau/Text.file','wb')
pickle.dump(a, output)
output.close()

v = list(a.values())    #nombre
k = list(a.keys())      #mots
mostSaidWords(v, k, 50)
#print v.index(max(v))
#print k[v.index(max(v))]
del k[v.index(max(v))]

