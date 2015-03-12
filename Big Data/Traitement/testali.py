from itertools import cycle
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from numpy.random import RandomState
import numpy as np
import pylab as pl
import numpy
import csv
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.svm.libsvm_sparse import sparse

def plot_2D(data, target, target_names):
    colors = cycle('rgbcmykw')
    target_ids = range(len(target_names))
    pl.figure()
    for i, c, label in zip(target_ids, colors, target_names):
        pl.scatter(data[target == i, 0], data[target == i, 1],
                    c=c, label=label)
    pl.legend()
    pl.show()


#ouvrir le fichier de texte
with open("/home/alexis/Bureau/Text.file") as f:
    content = f.readlines()
#with open("/home/alexis/Bureau/Text.file") as f:
#    content2 = f.readlines()
 
#transformer le fichier texte en matrice numerique
X = TfidfVectorizer().fit_transform(content)
X = X.toarray()
#Y = TfidfVectorizer().fit_transform(content2)
#Y = Y.toarray()


#Si vous voulez separer vos tweets en 3 classes:
km = KMeans(n_clusters=5, max_iter=1000).fit(X)
print km
classes=km.labels_ #classes va contenir une liste avec les nombres 0, 1 ,2 qui identifient les 3 classes
pca = PCA(n_components=2, whiten=True).fit(X)

X_pca = pca.transform(X)
plot_2D(X_pca, classes, ["c0", "c1","c2"])