from pymongo import MongoClient
import pymongo
from pymongo.collection import Collection
import re
from reportlab.graphics.barcode.eanbc import words
import pickle
from _dbus_bindings import Double
import math
from cmath import log
import copy

MONGO_DATABASE_NAME = 'twitter_db3'
MONGO_COLLECTION_NAME = 'twitter_collection3'

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

#Fonction permettant de recuperer le tweet dans la collection associee
def retrieveTwt(collection):
    for obj in collection.find({'text':{'$exists' : True}}):
        if obj:
            text = obj['text']
            print text
def LoadDictionnary(collection):
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

#Fonction donnant le dictionnaire associe a un tweet(ou chaine de caractere)
def OneTwtDictionnary(twt, dictionnary):
    dictionnary = {}
    words = twt.split()
    for word in range(len(words)):
        if dictionnary.has_key(words[word]):
            value = dictionnary[words[word]]
            dictionnary[words[word]] = value+1
        else: 
            dictionnary[words[word]] = 1               
    return dictionnary

#Fonction implementant un bubblesort (avec lien entre les index de la liste d'ocurrence et de la liste de mot)
def bubbleSortWordListOcurrenceList(occurencelist, wordlist):
    n = len(occurencelist)
    swapped_elements = True
    while swapped_elements == True:
        swapped_elements = False
        for j in range(0, n-1):
            if(occurencelist[j] < occurencelist[j+1]):
                swapped_elements = True
                occurencelist[j],occurencelist[j+1] = occurencelist[j+1],occurencelist[j]
                wordlist[j],wordlist[j+1] = wordlist[j+1],wordlist[j] 
#Fonction qui retourne les n mots les plus dit 
def mostSaidWords(occurencelist, wordlist, nbmots):
    n = len(occurencelist)
    if(nbmots < n):
        for j in range(0,nbmots-1):
            print wordlist[j]+' = '+str(occurencelist[j])
    else:
        print 'Pas assez de mots dans la liste'

#Fonction qui permet de calculer toutes les IDF des mots        
def allIDF(occurences, words, nbdocs):
    IDFlist = list(range(len(words)))
    for i in range(len(occurences)):
        nombredocscontaining = occurences[i]
        if(nombredocscontaining != 0):
            a = float(nbdocs)/nombredocscontaining
            a = math.log(a)+1
            IDFlist[i] = a
        else:
            print('ERREUR MATH DIVISION PAR 0')
    
    return IDFlist

    
def percentage(occurences):
    totaloccu = NbWords(occurences)
    percentlist = list(range(len(occurences)))
    if(totaloccu != 0):
        for i in range(len(occurences)):
                a = 100*float(occurences[i])/float(totaloccu)
                percentlist[i] = a
    else:
        print('ERREUR MATH DIVISION PAR 0')
    
    return percentlist
    
def invDocFrequency(collection, searchedword):
    IDF = 0
    nombredocs = collection.find().count()
    #print 'nombredocs = '+str(nombredocs)
    nombredocscontaining = 0
    #print 'containing = '+str(nombredocscontaining)
    if(nombredocscontaining != 0):
        a = float(nombredocs)/nombredocscontaining
        a = math.log(a)+1
        IDF = a
        #print 'IDF = '+str(IDF)
    else:
        print 'ERREUR MATH DIVISION PAR 0'
    return IDF

def cleanLists(listoccu, listword, listidf):
    i = len(listoccu)-1
    hastaglist =[]
    hastagoccu = []
    occurences = copy.deepcopy(listoccu)
    while(i >=0):
        if("#" in listword[i]):
            hastaglist.append(listword[i])
            hastagoccu.append(listoccu[i])
        
        if(occurences[i] < 4 or "#" in listword[i]):
            del listidf[i]
            del listoccu[i]
            del listword[i]
        i = i-1  
    print listoccu,listword,listidf,hastaglist,hastagoccu
    return listoccu,listword,listidf,hastaglist,hastagoccu

def NbWords(listoccu):
    return sum(listoccu) 

def moyenne(listoccu):
    moyenne = sum(listoccu)/len(listoccu)
    return moyenne

def interestingPos(thislist,moyenne):
    i = 0
    while(i < len(thislist)):
        if(thislist[i] < moyenne):
            return i-1       
        i = i+1   
    return i
  
def interestingWords(words, position,nbwords):
    interestwordlist = []
    i = position
    print 'position = '+str(position)
    for i in range(nbwords):
            if(position-i >= 0):
                #print words[position-i]
                #print position-i
                interestwordlist.append(words[position-i])
     
    return interestwordlist
  
client = MongoClient('localhost', 27017)
db = client[MONGO_DATABASE_NAME ]
collection = db[MONGO_COLLECTION_NAME]
nombredocs = collection.find().count()
a = dict()
a = LoadDictionnary(collection)
output = open('/home/alexis/Bureau/Text.file','wb')

occurence = list(a.values())    #nombre
words = list(a.keys())          #mots

bubbleSortWordListOcurrenceList(occurence, words)
IDF = allIDF(occurence, words, nombredocs)
 
table = cleanLists(occurence, words, IDF)
occurence = table[0]
words = table[1]
IDF = table[2]
hashtaglist = table[3]
hashtagoccu = table[4]

bubbleSortWordListOcurrenceList(hashtagoccu, hashtaglist)

print 'liste de mot :'
print words
print ''
print 'liste de hashtag :'
print hashtaglist
print ''
print 'liste des occurences :'
print occurence
#print 'liste de pourcentage (sur le nombre d\'occurence :'
#print percentage(occurence)
print ''
print 'liste des occurences (sur les hashtags) :'
print hashtagoccu
#print 'liste de pourcentage(sur les hashtags) :'
#print percentage(hashtagoccu)
position = interestingPos(occurence, moyenne(occurence))
#print interestingWords(words, position, 5)