# -*- coding: utf-8 -*-
from itertools import cycle
from sklearn.decomposition import PCA
from pymongo import MongoClient
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import re
import pylab as pl
#On importe les librairies

#Les informations pour se connecter à la base mongoDB et à la colection associée
MONGO_DATABASE_NAME = 'twitter'
MONGO_COLLECTION_NAME = 'twitter_collection3'
PATH = '/home/alexis/Bureau/Images'

#Fonction qui récupère le texte des tweets, retournant une liste des textes des tweets par cluster
def recup_cluster(collection):
    cluster0_list = []
    cluster1_list = []
    cluster2_list = []
    for obj in collection.find({'label':{'$exists' : True}}):
        print'recup'
        if obj:
            label = int(obj['label'])
            if(label == 0):
                cluster0_list.append(obj['text'])
            if(label == 1):
                cluster1_list.append(obj['text'])
            if(label == 2):
                cluster2_list.append(obj['text'])
    return cluster0_list,cluster1_list,cluster2_list

def LoadCluster(word, occurence):
    name = []
    data = []
    for i in range(0, 5):
        name.append(word[i])
        data.append(occurence[i])
    return name, data
        
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
    pl.figure(1).savefig(PATH+'CLUSTER_TEXT.png')
    pl.show()

#On se connecte a MONgoDb et on utilise la collection associée
client = MongoClient('mongodb://zaka:zaka@ds061767.mongolab.com:61767/twitter')
db = client[MONGO_DATABASE_NAME]
collection = db[MONGO_COLLECTION_NAME]
print'ok'

#ouvrir le fichier de texte
with open("/home/alexis/Bureau/Text.file") as ftext:
    print'ok'
    contentext = ftext.readlines()
    print contentext
    print 'merde'

print 'zboub'
#transformer le fichier texte en matrice numerique
X = TfidfVectorizer().fit_transform(contentext)
X = X.toarray()

#On fait un essaie en separerant nos tweets en 3 classes:
kmX = KMeans(n_clusters=3, max_iter=300).fit(X)

#classes va contenir une liste avec les nombres 0, 1 ,2 qui identifient les 3 classes
classes=kmX.labels_ 
print'ok'

#On update les labels dans mongoDB
for index, tweets in enumerate(collection.find()):
        print'connection'
        if tweets:
            identi = tweets['_id']
            collection.update({'_id': identi},{'$set': {'label': str(classes[index])}})
          
pca = PCA(whiten=True).fit(X)
X_pca = pca.transform(X)

cluster = []
#On récupère le texte de chaque tweet pour chaque cluster
recupcluster = recup_cluster(collection)
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

plot_2D(X_pca, classes, ["c0", "c1","c2"])



cluster=LoadCluster(words1, occurence1)

plt.figure(1)
plt.pie(cluster[1], labels=cluster[0], autopct='%1.1f%%', shadow=True)
plt.axis('equal')
plt.figure(1).savefig(PATH+'C1_text.png') 


cluster1=LoadCluster(words2, occurence2)

plt.figure(2)
plt.pie(cluster1[1], labels=cluster1[0], autopct='%1.1f%%', shadow=True)
plt.axis('equal')
plt.figure(1).savefig(PATH+'C2_text.png') 

plt.figure(3)


cluster2=LoadCluster(words0, occurence0)

plt.pie(cluster2[1], labels=cluster2[0], autopct='%1.1f%%', shadow=True)
plt.axis('equal')
plt.figure(1).savefig(PATH+'C3_text.png') 

plt.show()


