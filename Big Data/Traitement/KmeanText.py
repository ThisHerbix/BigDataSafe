from itertools import cycle
from sklearn.decomposition import PCA
from pymongo import MongoClient
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import re

import pylab as pl

MONGO_DATABASE_NAME = 'twitter_db3'
MONGO_COLLECTION_NAME = 'twitter_collection3'
PATH = '/Users/K2/Desktop/'

def recup_cluster(collection):
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

def plot_2D(data, target, target_names):
    colors = cycle('rgbcmykw')
    target_ids = range(len(target_names))
    pl.figure()
    for i, c, label in zip(target_ids, colors, target_names):
        pl.scatter(data[target == i, 0], data[target == i, 1],
                    c=c, label=label)
    pl.legend()
    pl.show()

client = MongoClient('localhost', 27017)
db = client[MONGO_DATABASE_NAME]
collection = db[MONGO_COLLECTION_NAME]

#ouvrir le fichier de texte
with open("/Users/K2/Desktop/Text.file") as ftext:
    contentext = ftext.readlines()
#with open("/home/alexis/Bureau/Text.file") as f:
#    content2 = f.readlines()
 
#transformer le fichier texte en matrice numerique
X = TfidfVectorizer().fit_transform(contentext)
X = X.toarray()

#MinibatchKmeans
#Si vous voulez separer vos tweets en 3 classes:

kmX = KMeans(n_clusters=3, max_iter=300).fit(X)


classes=kmX.labels_ #classes va contenir une liste avec les nombres 0, 1 ,2 qui identifient les 3 classes

for index, tweets in enumerate(collection.find()):
        if tweets:
            identi = tweets['_id']
            collection.update({'_id': identi},{'$set': {'label': str(classes[index])}})
            
pca = PCA(whiten=True).fit(X)
X_pca = pca.transform(X)

cluster = []
recupcluster = recup_cluster(collection)
dictionnary0 = LoadDictionnary(recupcluster[0])
dictionnary1 = LoadDictionnary(recupcluster[1])
dictionnary2 = LoadDictionnary(recupcluster[2])
occurence0 = list(dictionnary0.values())    #nombre
occurence1 = list(dictionnary1.values())
occurence2 = list(dictionnary2.values())
words0 = list(dictionnary0.keys())          
words1 = list(dictionnary1.keys()) 
words2 = list(dictionnary2.keys()) 
bubbleSortWordListOcurrenceList(occurence0, words0)
bubbleSortWordListOcurrenceList(occurence1, words1)
bubbleSortWordListOcurrenceList(occurence2, words2)
print occurence0
print words0

print occurence1
print words1
print occurence2
print words2

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



