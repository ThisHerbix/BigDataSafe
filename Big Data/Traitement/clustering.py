#from sklearn.datasets import load_iris
from itertools import cycle
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from numpy.random import RandomState
import numpy as np
import pylab as pl

class clustering:
    def __init__(self):
        v1 = np.random.randint(10, size=(300,200))
        v2 = np.random.randint(10, size=(300,200))      
        m = np.vstack((v1, v2))
        print m
        self.plot(m)
        #print load_iris().data

    def plot(self, X):
        pca = PCA(n_components=2, whiten=True).fit(X)
        X_pca = pca.transform(X)
        #rng = RandomState(42)
        kmeans = KMeans(n_clusters=2, random_state=RandomState(42)).fit(X_pca)
        plot_2D(X_pca, kmeans.labels_, ["c0", "c1"])

def plot_2D(data, target, target_names):
    colors = cycle('rgbcmykw')
    target_ids = range(len(target_names))
    pl.figure()
    for i, c, label in zip(target_ids, colors, target_names):
        pl.scatter(data[target == i, 0], data[target == i, 1],
                    c=c, label=label)
    pl.legend()
    pl.show()

if __name__ == '__main__':
    print 2
    c = clustering()