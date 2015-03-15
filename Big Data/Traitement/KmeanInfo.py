from itertools import cycle
from sklearn.decomposition import PCA
from pymongo import MongoClient
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import re
import pylab as pl
import matplotlib.pyplot as plt

SEPARATOR = ' '
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
            a = SEPARATOR+str(sum(obj['nbwords']))+SEPARATOR+str(len(obj['hashtag']))+SEPARATOR+str(obj['horary'])+SEPARATOR+str(obj['day'])+SEPARATOR+str(obj['daynumber'])+SEPARATOR+str(obj['month'])+SEPARATOR+str(obj['year'])+SEPARATOR+str(obj['favorite_count'])+SEPARATOR+str(obj['retweeted'])+SEPARATOR+str(obj['favorited'])+SEPARATOR+str(obj['user_activity'])+'\n'
            if(label == 0):
                cluster0_list.append(a)
            if(label == 1):
                cluster1_list.append(a)
            if(label == 2):
                cluster2_list.append(a)
    return cluster0_list,cluster1_list,cluster2_list

def LoadCluster(word, occurence):
    name = []
    data = []
    if(len(word) >= 5):
        j = 5
    elif(len(word) >= 4):
        j = 4
    elif(len(word) >= 3):
        j = 3
    elif(len(word) >= 2):
        j = 2
    else:
        j = 1
    for i in range(0, j):
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
def ToGraph(listx):
    dicti =  LoadDictionnary(listx)
    listvalue = list(dicti.keys())
    occurence = list(dicti.values())
    bubbleSortWordListOcurrenceList(occurence, listvalue)
    return occurence, listvalue



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
with open("/Users/K2/Desktop/Info.file") as f:
    content = f.readlines()
#with open("/home/alexis/Bureau/Text.file") as f:
#    content2 = f.readlines()
 
#transformer le fichier texte en matrice numerique
X = TfidfVectorizer().fit_transform(content)
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
infocluster0 = [info.replace('\n', ' ') for info in recupcluster[0]]
infocluster1 = [info.replace('\n', ' ') for info in recupcluster[1]]
infocluster2 = [info.replace('\n', ' ') for info in recupcluster[2]]

infotab0 = [info.split(' ') for info in infocluster0]
retrieve0 = retrieveInfo(infotab0)
infotab1 = [info.split(' ') for info in infocluster1]
retrieve1 = retrieveInfo(infotab1)
infotab2 = [info.split(' ') for info in infocluster2]
retrieve2 = retrieveInfo(infotab2)

plot_2D(X_pca, classes, ["c0", "c1","c2"])

#nbword, nbhashtag, heure, day, daynumber,month,year,favorite_count,retweeted,favorited,user_activity

#PREMIER CLUSTER

nbwordsoccurence0  = ToGraph(retrieve0[0])[0]
nbwords0 =  ToGraph(retrieve0[0])[1] 

cluster=LoadCluster(nbwords0, nbwordsoccurence0)

plt.figure(1)
plt.pie(cluster[1], labels=cluster[0], autopct='%1.1f%%', shadow=True)
plt.axis('equal')
plt.title('Cluster1: nbWords')
plt.figure(1).savefig(PATH+'C1_1_info.png')          

nbhashtagoccurence0 =  ToGraph(retrieve0[1])[0]
nbhashtag0 =  ToGraph(retrieve0[1])[1]

cluster1=LoadCluster(nbhashtag0, nbhashtagoccurence0)

plt.figure(2)
plt.pie(cluster1[1], labels=cluster1[0], autopct='%1.1f%%', shadow=True)
plt.axis('equal')
plt.title('Cluster1: nbHashtag')
plt.figure(2).savefig(PATH+'C1_2_info.png')  

heureoccurence0 =  ToGraph(retrieve0[2])[0]
heure0 =  ToGraph(retrieve0[2])[1]
print heureoccurence0
print heure0

cluster2=LoadCluster(heure0, heureoccurence0)

plt.figure(3)
plt.pie(cluster2[1], labels=cluster2[0], autopct='%1.1f%%', shadow=True)
plt.axis('equal') 
plt.title('Cluster1: Hours')
plt.figure(3).savefig(PATH+'C1_3_info.png')


dayoccurence0 =  ToGraph(retrieve0[3])[0]
day0 = ToGraph(retrieve0[3])[1]

cluster3=LoadCluster(day0, dayoccurence0)

plt.figure(4)
plt.pie(cluster3[1], labels=cluster3[0], autopct='%1.1f%%', shadow=True)
plt.axis('equal') 
plt.title('Cluster1: Days') 
plt.figure(4).savefig(PATH+'C1_4_info.png')


daynumberoccurence0 =  ToGraph(retrieve0[4])[0]
daynumber0 =  ToGraph(retrieve0[4])[1]

cluster4=LoadCluster(daynumber0, daynumberoccurence0)

plt.figure(5)
plt.pie(cluster4[1], labels=cluster4[0], autopct='%1.1f%%', shadow=True)
plt.axis('equal') 
plt.title('Cluster1: DayNumber') 
plt.figure(5).savefig(PATH+'C1_5_info.png')

monthoccurence0 =  ToGraph(retrieve0[5])[0]
month0 =  ToGraph(retrieve0[5])[1]

cluster5=LoadCluster(month0, monthoccurence0)

plt.figure(6)
plt.pie(cluster5[1], labels=cluster5[0], autopct='%1.1f%%', shadow=True)
plt.axis('equal') 
plt.title('Cluster1: Month') 
plt.figure(6).savefig(PATH+'C1_6_info.png')


yearoccurence0 =  ToGraph(retrieve0[6])[0]
year0 =  ToGraph(retrieve0[6])[1]

cluster6=LoadCluster(year0, yearoccurence0)

plt.figure(7)
plt.pie(cluster6[1], labels=cluster6[0], autopct='%1.1f%%', shadow=True)
plt.axis('equal') 
plt.title('Cluster1: Year') 
plt.figure(7).savefig(PATH+'C1_7_info.png')

favorite_countoccurence0 =  ToGraph(retrieve0[7])[0]
favorite_count0 =  ToGraph(retrieve0[7])[1]

cluster7=LoadCluster(favorite_count0, favorite_countoccurence0)

plt.figure(8)
plt.pie(cluster7[1], labels=cluster7[0], autopct='%1.1f%%', shadow=True)
plt.axis('equal') 
plt.title('Cluster1: nbFavorite') 
plt.figure(8).savefig(PATH+'C1_8_info.png')


retweetedoccurence0 =  ToGraph(retrieve0[8])[0]
retweeted0 =  ToGraph(retrieve0[8])[1]

cluster8=LoadCluster(retweeted0, retweetedoccurence0)

plt.figure(9)
plt.pie(cluster8[1], labels=cluster8[0], autopct='%1.1f%%', shadow=True)
plt.axis('equal') 
plt.title('Cluster1: Retweeted')
plt.figure(9).savefig(PATH+'C1_9_info.png')
 

favoritedoccurence0 =  ToGraph(retrieve0[9])[0]
favorited0 =  ToGraph(retrieve0[9])[1]

cluster9=LoadCluster(favorited0, favoritedoccurence0)

plt.figure(10)
plt.pie(cluster9[1], labels=cluster9[0], autopct='%1.1f%%', shadow=True)
plt.axis('equal') 
plt.title('Cluster1: Favorited') 
plt.figure(10).savefig(PATH+'C1_10_info.png')


user_activityoccurence0 = ToGraph(retrieve0[10])[0]
user_activity0 =  ToGraph(retrieve0[10])[1]

cluster10=LoadCluster(user_activity0, user_activityoccurence0)

plt.figure(11)
plt.pie(cluster10[1], labels=cluster10[0], autopct='%1.1f%%', shadow=True)
plt.axis('equal') 
plt.title('Cluster1: UserActivity') 
plt.figure(11).savefig(PATH+'C1_11_info.png')

#DEUXIEME CLUSTER

nbwordsoccurence1  = ToGraph(retrieve1[0])[0]
nbwords1 =  ToGraph(retrieve1[0])[1]

cluster11=LoadCluster(nbwords1, nbwordsoccurence1)

plt.figure(12)
plt.pie(cluster11[1], labels=cluster11[0], autopct='%1.1f%%', shadow=True)
plt.axis('equal')  
plt.title('Cluster2: nbWords') 
plt.figure(12).savefig(PATH+'C2_1_info.png')           

nbhashtagoccurence1 =  ToGraph(retrieve1[1])[0]
nbhashtag1 =  ToGraph(retrieve1[1])[1]

cluster12=LoadCluster(nbhashtag1, nbhashtagoccurence1)

plt.figure(13)
plt.pie(cluster12[1], labels=cluster12[0], autopct='%1.1f%%', shadow=True)
plt.axis('equal')
plt.title('Cluster2: nbHashtag') 
plt.figure(13).savefig(PATH+'C2_2_info.png')           


heureoccurence1 =  ToGraph(retrieve1[2])[0]
heure1 =  ToGraph(retrieve1[2])[1]

cluster13=LoadCluster(heure1, heureoccurence1)

plt.figure(14)
plt.pie(cluster13[1], labels=cluster13[0], autopct='%1.1f%%', shadow=True)
plt.axis('equal') 
plt.title('Cluster2: Hours')
plt.figure(14).savefig(PATH+'C2_3_info.png')           


dayoccurence1 =  ToGraph(retrieve1[3])[0]
day1 = ToGraph(retrieve1[3])[1]

cluster14=LoadCluster(day1, dayoccurence1)

plt.figure(15)
plt.pie(cluster14[1], labels=cluster14[0], autopct='%1.1f%%', shadow=True)
plt.axis('equal') 
plt.title('Cluster2: Days')
plt.figure(15).savefig(PATH+'C2_4_info.png')           


daynumberoccurence1 =  ToGraph(retrieve1[4])[0]
daynumber1 =  ToGraph(retrieve1[4])[1]

cluster15=LoadCluster(daynumber1, daynumberoccurence1)

plt.figure(16)
plt.pie(cluster15[1], labels=cluster15[0], autopct='%1.1f%%', shadow=True)
plt.axis('equal') 
plt.title('Cluster2: DayNumber')
plt.figure(16).savefig(PATH+'C2_5_info.png')           


monthoccurence1 =  ToGraph(retrieve1[5])[0]
month1 =  ToGraph(retrieve1[5])[1]

cluster16=LoadCluster(month1, monthoccurence1)

plt.figure(17)
plt.pie(cluster16[1], labels=cluster16[0], autopct='%1.1f%%', shadow=True)
plt.axis('equal') 
plt.title('Cluster2: Months')
plt.figure(17).savefig(PATH+'C2_6_info.png')           


yearoccurence1 =  ToGraph(retrieve1[6])[0]
year1 =  ToGraph(retrieve1[6])[1]

cluster17=LoadCluster(year1, yearoccurence1)

plt.figure(18)
plt.pie(cluster17[1], labels=cluster17[0], autopct='%1.1f%%', shadow=True)
plt.axis('equal') 
plt.title('Cluster2: Years')
plt.figure(18).savefig(PATH+'C2_7_info.png')           


favorite_countoccurence1 =  ToGraph(retrieve1[7])[0]
favorite_count1 =  ToGraph(retrieve1[7])[1]

cluster18=LoadCluster(favorite_count1, favorite_countoccurence1)

plt.figure(19)
plt.pie(cluster18[1], labels=cluster18[0], autopct='%1.1f%%', shadow=True)
plt.axis('equal') 
plt.title('Cluster2: nbFavorite')
plt.figure(19).savefig(PATH+'C2_8_info.png')           


retweetedoccurence1 =  ToGraph(retrieve1[8])[0]
retweeted1 =  ToGraph(retrieve1[8])[1]

cluster19=LoadCluster(retweeted1, retweetedoccurence1)

plt.figure(20)
plt.pie(cluster19[1], labels=cluster19[0], autopct='%1.1f%%', shadow=True)
plt.axis('equal')
plt.title('Cluster2: Retweeted') 
plt.figure(20).savefig(PATH+'C2_9_info.png')           


favoritedoccurence1 =  ToGraph(retrieve1[9])[0]
favorited1 =  ToGraph(retrieve1[9])[1]

cluster20=LoadCluster(favorited1, favoritedoccurence1)

plt.figure(21)
plt.pie(cluster20[1], labels=cluster20[0], autopct='%1.1f%%', shadow=True)
plt.axis('equal') 
plt.title('Cluster2: Favorited')
plt.figure(21).savefig(PATH+'C2_10_info.png')           


user_activityoccurence1 = ToGraph(retrieve1[10])[0]
user_activity1 =  ToGraph(retrieve1[10])[1]

cluster21=LoadCluster(user_activity1, user_activityoccurence1)

plt.figure(22)
plt.pie(cluster21[1], labels=cluster21[0], autopct='%1.1f%%', shadow=True)
plt.axis('equal') 
plt.title('Cluster2: UserActivity')
plt.figure(22).savefig(PATH+'C2_11_info.png')           


#TROISIEME CLUSTER


nbwordsoccurence2  = ToGraph(retrieve2[0])[0]
nbwords2 =  ToGraph(retrieve2[0])[1]

cluster22=LoadCluster(nbwords2, nbwordsoccurence2)

plt.figure(23)
plt.pie(cluster22[1], labels=cluster22[0], autopct='%1.1f%%', shadow=True)
plt.axis('equal')   
plt.title('Cluster3: nbWords')  
plt.figure(23).savefig(PATH+'C3_1_info.png')           
      

nbhashtagoccurence2 =  ToGraph(retrieve2[1])[0]
nbhashtag2 =  ToGraph(retrieve2[1])[1]

cluster23=LoadCluster(nbhashtag2, nbhashtagoccurence2)

plt.figure(24)
plt.pie(cluster23[1], labels=cluster23[0], autopct='%1.1f%%', shadow=True)
plt.axis('equal') 
plt.title('Cluster3: nbHashtag') 
plt.figure(24).savefig(PATH+'C3_2_info.png')  

heureoccurence2 =  ToGraph(retrieve2[2])[0]
heure2 =  ToGraph(retrieve2[2])[1]

cluster24=LoadCluster(heure2, heureoccurence2)

plt.figure(25)
plt.pie(cluster24[1], labels=cluster24[0], autopct='%1.1f%%', shadow=True)
plt.axis('equal') 
plt.title('Cluster3: Hours')
plt.figure(25).savefig(PATH+'C3_3_info.png')   

dayoccurence2 =  ToGraph(retrieve2[3])[0]
day2 = ToGraph(retrieve2[3])[1]

cluster25=LoadCluster(day2, dayoccurence2)

plt.figure(26)
plt.pie(cluster25[1], labels=cluster25[0], autopct='%1.1f%%', shadow=True)
plt.axis('equal') 
plt.title('Cluster3: Days')  
plt.figure(26).savefig(PATH+'C3_4_info.png') 

daynumberoccurence2 =  ToGraph(retrieve2[4])[0]
daynumber2 =  ToGraph(retrieve2[4])[1]

cluster26=LoadCluster(daynumber2, daynumberoccurence2)

plt.figure(27)
plt.pie(cluster26[1], labels=cluster26[0], autopct='%1.1f%%', shadow=True)
plt.axis('equal') 
plt.title('Cluster3: DayNumber')
plt.figure(27).savefig(PATH+'C3_5_info.png')   

monthoccurence2 =  ToGraph(retrieve2[5])[0]
month2 =  ToGraph(retrieve2[5])[1]

cluster27=LoadCluster(month2, monthoccurence2)

plt.figure(28)
plt.pie(cluster27[1], labels=cluster27[0], autopct='%1.1f%%', shadow=True)
plt.axis('equal') 
plt.title('Cluster3: Months') 
plt.figure(28).savefig(PATH+'C3_6_info.png')  

yearoccurence2 =  ToGraph(retrieve2[6])[0]
year2 =  ToGraph(retrieve2[6])[1]

cluster28=LoadCluster(year2, yearoccurence2)

plt.figure(29)
plt.pie(cluster28[1], labels=cluster28[0], autopct='%1.1f%%', shadow=True)
plt.axis('equal') 
plt.title('Cluster3: Years') 
plt.figure(29).savefig(PATH+'C3_7_info.png')  

favorite_countoccurence2 =  ToGraph(retrieve2[7])[0]
favorite_count2 =  ToGraph(retrieve2[7])[1]

cluster29=LoadCluster(favorite_count2, favorite_countoccurence2)

plt.figure(30)
plt.pie(cluster29[1], labels=cluster29[0], autopct='%1.1f%%', shadow=True)
plt.axis('equal') 
plt.title('Cluster3: nbFavorite') 
plt.figure(30).savefig(PATH+'C3_8_info.png')  

retweetedoccurence2 =  ToGraph(retrieve2[8])[0]
retweeted2 =  ToGraph(retrieve2[8])[1]

cluster30=LoadCluster(retweeted2, retweetedoccurence2)

plt.figure(31)
plt.pie(cluster30[1], labels=cluster30[0], autopct='%1.1f%%', shadow=True)
plt.axis('equal') 
plt.title('Cluster3: Retweeted') 
plt.figure(31).savefig(PATH+'C3_9_info.png')  

favoritedoccurence2 =  ToGraph(retrieve2[9])[0]
favorited2 =  ToGraph(retrieve2[9])[1]

cluster31=LoadCluster(favorited2, favoritedoccurence2)

plt.figure(32)
plt.pie(cluster31[1], labels=cluster31[0], autopct='%1.1f%%', shadow=True)
plt.axis('equal') 
plt.title('Cluster3: Favorited')  
plt.figure(32).savefig(PATH+'C3_10_info.png') 

user_activityoccurence2 = ToGraph(retrieve2[10])[0]
user_activity2 =  ToGraph(retrieve2[10])[1]

cluster32=LoadCluster(user_activity2, user_activityoccurence2)

plt.figure(33)
plt.pie(cluster32[1], labels=cluster32[0], autopct='%1.1f%%', shadow=True)
plt.axis('equal')
plt.title('Cluster3: UserActivity') 
plt.figure(33).savefig(PATH+'C3_11_info.png')  
plt.show()