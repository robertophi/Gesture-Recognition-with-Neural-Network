import matplotlib.pyplot as plt
from matplotlib import style
import numpy as np
from sklearn.cluster import KMeans
import random
style.use('ggplot')

#ORIGINAL:

X = np.zeros([100,2])
for i in range(0,50):
    X[i,0] = 5+random.randint(0,10)/2
    X[i,1] = -5+random.randint(0,10)/2
for i in range(50,100):
    X[i,0] = -5+random.randint(0,10)/2
    X[i,1] = 5+random.randint(0,10)/2


plt.scatter(X[:, 0],X[:, 1], s=150, linewidths = 1, zorder = 10)
plt.show()


clf = KMeans(n_clusters=2)
clf.fit(X)

centroids = clf.cluster_centers_
labels = clf.labels_


plt.scatter(centroids[:, 0],centroids[:, 1], marker = "x", s=150, linewidths = 5, zorder = 10)
plt.show()