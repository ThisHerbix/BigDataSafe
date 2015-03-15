# -*- coding: utf-8 -*-
from itertools import cycle
from sklearn.decomposition import PCA
from pymongo import MongoClient
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import re
import pylab as pl
#On importe les librairies

#Les informations pour se connecter à la base mongoDB et à la colection associée
MONGO_DATABASE_NAME = 'twitter_db3'
MONGO_COLLECTION_NAME = 'twitter_collection3'
SEPARATOR = ' '

#Fonction qui récupère le texte des tweets, retournant une liste des textes des tweets par cluster
def recup_clusterText(collection):
    cluster0_list = []
    cluster1_list = []
    cluster2_list = []
    for obj in collection.find({'label':{'$exists' : True}}):
        if obj:
            label = int(obj['label'])
            if(label == 0):
                cluster0_list.append(obj['text'])
            if(label == 1):
                cluster1_list.append(obj['text'])
            if(label == 2):
                cluster2_list.append(obj['text'])
    return cluster0_list,cluster1_list,cluster2_list

#Fonction qui récupère les informations liées aux tweets, retournant une liste des textes des tweets par cluster
def recup_clusterInfo(collection):
    cluster0_list = []
    cluster1_list = []
    cluster2_list = []
    for obj in collection.find({'label':{'$exists' : True}}):
        if obj:
            label = int(obj['label'])
            a = SEPARATOR+str(sum(obj['nbwords']))+SEPARATOR+str(len(obj['hashtag']))+SEPARATOR+str(obj['horary'])+SEPARATOR+str(obj['day'])+SEPARATOR+str(obj['daynumber'])+SEPARATOR+str(obj['month'])+SEPARATOR+str(obj['year'])+SEPARATOR+str(obj['favorite_count'])+SEPARATOR+str(obj['retweeted'])+SEPARATOR+str(obj['favorited'])+SEPARATOR+str(obj['user_activity'])+'\n'
            if(label == 0):
                cluster0_list.append(a)
            if(label == 1):
                cluster1_list.append(a)
            if(label == 2):
                cluster2_list.append(a)
    return cluster0_list,cluster1_list,cluster2_list

#Fonction qui charge un dictionnaire de type "mot : nombre de fois que le mot est apparu".
#On utilisera cette fonction par la suite ur obtenir un dictionnaire par cluster
def LoadDictionnary(cluster_list):
    dictionnary = {}
    for obj in cluster_list:
        if obj:
            words = re.split(r'[,; _\/\\]*',obj)
            for word in range(len(words)):
                if dictionnary.has_key(words[word]):
                    value = dictionnary[words[word]]
                    dictionnary[words[word]] = value+1
                else: 
                    dictionnary[words[word]] = 1   
    return dictionnary

#On créée des liste contenants les informations d'un cluster
def retrieveInfo(cluster_infotab):
    heure = []
    nbword = []
    nbhashtag = []
    day = []
    daynumber = []
    month = []
    year = []
    favorite_count = []
    retweeted = []
    favorited = []
    user_activity = []
    for tab in cluster_infotab:
        nbword.append(tab[1])
        nbhashtag.append(tab[2])
        heure.append(tab[3])
        day.append(tab[4])
        daynumber.append(tab[5])
        month.append(tab[6])
        year.append(tab[7])
        favorite_count.append(tab[8])
        retweeted.append(tab[9])
        favorited.append(tab[10])
        user_activity.append(tab[11])
    return nbword, nbhashtag, heure, day, daynumber,month,year,favorite_count,retweeted,favorited,user_activity

#Fonction qui retourne deux listes servant à plot des graphes  
def ToGraph(listx):
    dicti =  LoadDictionnary(listx)
    listvalue = list(dicti.keys())
    occurence = list(dicti.values())
    SortWordListOcurrenceList(occurence, listvalue)
    return occurence, listvalue

#Fonction qui tri la liste de mots et la liste d'occurence par nombre de fois que le mot est apparu
def SortWordListOcurrenceList(occurencelist, wordlist):
    n = len(occurencelist)
    swapped_elements = True
    while swapped_elements == True:
        swapped_elements = False
        for j in range(0, n-1):
            if(occurencelist[j] < occurencelist[j+1]):
                swapped_elements = True
                occurencelist[j],occurencelist[j+1] = occurencelist[j+1],occurencelist[j]
                wordlist[j],wordlist[j+1] = wordlist[j+1],wordlist[j]

#Fonction qui trace u graphe dans un espace 2D
def plot_2D(data, target, target_names):
    colors = cycle('rgbcmykw')
    target_ids = range(len(target_names))
    pl.figure()
    for i, c, label in zip(target_ids, colors, target_names):
        pl.scatter(data[target == i, 0], data[target == i, 1],
                    c=c, label=label)
    pl.legend()
    pl.show()

#On se connecte a MONgoDb et on utilise la collection associée
client = MongoClient('localhost', 27017)
db = client[MONGO_DATABASE_NAME]
collection = db[MONGO_COLLECTION_NAME]

#ouvrir le fichier de texte
with open("/home/alexis/Bureau/Text.file") as ftext:
    contentext = ftext.readlines()

#transformer le fichier texte en matrice numerique
X = TfidfVectorizer().fit_transform(contentext)
X = X.toarray()

#ouvrir le fichier d'information
with open("/home/alexis/Bureau/Info.file") as finfo:
    contentinfo = finfo.readlines()
Y = TfidfVectorizer().fit_transform(contentinfo)
Y = Y.toarray()

#on associe les deux matrices
Z = np.column_stack((X,Y))



kmZ = KMeans(n_clusters=3, max_iter=300).fit(Z)

#classes va contenir une liste avec les nombres 0, 1 ,2 qui identifient les 3 classes
classes=kmZ.labels_

for index, tweets in enumerate(collection.find()):
        if tweets:
            identi = tweets['_id']
            collection.update({'_id': identi},{'$set': {'label': str(classes[index])}})
            
pca = PCA(whiten=True).fit(Z)
Z_pca = pca.transform(Z)

#On récupère le texte de chaque tweet pour chaque cluster
cluster = []
recupcluster = recup_clusterText(collection)
#on charge les dictionnaires pour chaque cluster
dictionnary0 = LoadDictionnary(recupcluster[0])
dictionnary1 = LoadDictionnary(recupcluster[1])
dictionnary2 = LoadDictionnary(recupcluster[2])
#On récupère les nombres de fois que chaque mots apparaît
occurence0 = list(dictionnary0.values())
occurence1 = list(dictionnary1.values())
occurence2 = list(dictionnary2.values())
#On récupère les mots
words0 = list(dictionnary0.keys())          
words1 = list(dictionnary1.keys()) 
words2 = list(dictionnary2.keys())
#On trie les listes
SortWordListOcurrenceList(occurence0, words0)
SortWordListOcurrenceList(occurence1, words1)
SortWordListOcurrenceList(occurence2, words2)

#On récupère les informations de chaque tweet pour chaque cluster
recupcluster = recup_clusterInfo(collection)
infocluster0 = [info.replace('\n', ' ') for info in recupcluster[0]]
infocluster1 = [info.replace('\n', ' ') for info in recupcluster[1]]
infocluster2 = [info.replace('\n', ' ') for info in recupcluster[2]]

#On découpe ces information en liste
infotab0 = [info.split(' ') for info in infocluster0]
retrieve0 = retrieveInfo(infotab0)
infotab1 = [info.split(' ') for info in infocluster1]
retrieve1 = retrieveInfo(infotab1)
infotab2 = [info.split(' ') for info in infocluster2]
retrieve2 = retrieveInfo(infotab2)

#Pour chaque cluster on récupère toutes les informations de manière à pouvoir ensuite les tracer dans un espace 2D
#PREMIER CLUSTER

nbwordsoccurence0  = ToGraph(retrieve0[0])[0]
nbwords0 =  ToGraph(retrieve0[0])[1]            

nbhashtagoccurence0 =  ToGraph(retrieve0[1])[0]
nbhashtag0 =  ToGraph(retrieve0[1])[1]

heureoccurence0 =  ToGraph(retrieve0[2])[0]
heure0 =  ToGraph(retrieve0[2])[1]

dayoccurence0 =  ToGraph(retrieve0[3])[0]
day0 = ToGraph(retrieve0[3])[1]

daynumberoccurence0 =  ToGraph(retrieve0[4])[0]
daynumber0 =  ToGraph(retrieve0[4])[1]

monthoccurence0 =  ToGraph(retrieve0[5])[0]
month0 =  ToGraph(retrieve0[5])[1]

yearoccurence0 =  ToGraph(retrieve0[6])[0]
year0 =  ToGraph(retrieve0[6])[1]

favorite_countoccurence0 =  ToGraph(retrieve0[7])[0]
favorite_count0 =  ToGraph(retrieve0[7])[1]

retweetedoccurence0 =  ToGraph(retrieve0[8])[0]
retweeted0 =  ToGraph(retrieve0[8])[1]

favoritedoccurence0 =  ToGraph(retrieve0[9])[0]
favorited0 =  ToGraph(retrieve0[9])[1]

user_activityoccurence0 = ToGraph(retrieve0[10])[0]
user_activity0 =  ToGraph(retrieve0[10])[1]

#DEUXIEME CLUSTER

nbwordsoccurence1  = ToGraph(retrieve1[0])[0]
nbwords1 =  ToGraph(retrieve1[0])[1]            

nbhashtagoccurence1 =  ToGraph(retrieve1[1])[0]
nbhashtag1 =  ToGraph(retrieve1[1])[1]

heureoccurence1 =  ToGraph(retrieve1[2])[0]
heure1 =  ToGraph(retrieve1[2])[1]

dayoccurence1 =  ToGraph(retrieve1[3])[0]
day1 = ToGraph(retrieve1[3])[1]

daynumberoccurence1 =  ToGraph(retrieve1[4])[0]
daynumber1 =  ToGraph(retrieve1[4])[1]

monthoccurence1 =  ToGraph(retrieve1[5])[0]
month1 =  ToGraph(retrieve1[5])[1]

yearoccurence1 =  ToGraph(retrieve1[6])[0]
year1 =  ToGraph(retrieve1[6])[1]

favorite_countoccurence1 =  ToGraph(retrieve1[7])[0]
favorite_count1 =  ToGraph(retrieve1[7])[1]

retweetedoccurence1 =  ToGraph(retrieve1[8])[0]
retweeted1 =  ToGraph(retrieve1[8])[1]

favoritedoccurence1 =  ToGraph(retrieve1[9])[0]
favorited1 =  ToGraph(retrieve1[9])[1]

user_activityoccurence1 = ToGraph(retrieve1[10])[0]
user_activity1 =  ToGraph(retrieve1[10])[1]

#TROISIEME CLUSTER


nbwordsoccurence2  = ToGraph(retrieve2[0])[0]
nbwords2 =  ToGraph(retrieve2[0])[1]            

nbhashtagoccurence2 =  ToGraph(retrieve2[1])[0]
nbhashtag2 =  ToGraph(retrieve2[1])[1]

heureoccurence2 =  ToGraph(retrieve2[2])[0]
heure2 =  ToGraph(retrieve2[2])[1]

dayoccurence2 =  ToGraph(retrieve2[3])[0]
day2 = ToGraph(retrieve2[3])[1]

daynumberoccurence2 =  ToGraph(retrieve2[4])[0]
daynumber2 =  ToGraph(retrieve2[4])[1]

monthoccurence2 =  ToGraph(retrieve2[5])[0]
month2 =  ToGraph(retrieve2[5])[1]

yearoccurence2 =  ToGraph(retrieve2[6])[0]
year2 =  ToGraph(retrieve2[6])[1]

favorite_countoccurence2 =  ToGraph(retrieve2[7])[0]
favorite_count2 =  ToGraph(retrieve2[7])[1]

retweetedoccurence2 =  ToGraph(retrieve2[8])[0]
retweeted2 =  ToGraph(retrieve2[8])[1]

favoritedoccurence2 =  ToGraph(retrieve2[9])[0]
favorited2 =  ToGraph(retrieve2[9])[1]

user_activityoccurence2 = ToGraph(retrieve2[10])[0]
user_activity2 =  ToGraph(retrieve2[10])[1]

plot_2D(Z_pca, classes, ["c0", "c1","c2"])