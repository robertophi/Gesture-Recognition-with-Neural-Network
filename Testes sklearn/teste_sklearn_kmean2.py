import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import style
import numpy as np
from sklearn.cluster import KMeans
import random
style.use('ggplot')

#ORIGINAL:

X = np.zeros([100,3])
for i in range(0,50):
    X[i,0] = 5+random.randint(0,10)/2
    X[i,1] = -5+random.randint(0,10)/2
    X[i, 2] =  random.randint(0, 10) / 2
for i in range(50,100):
    X[i,0] = -5+random.randint(0,10)/2
    X[i,1] = 5+random.randint(0,10)/2
    X[i,2] = random.randint(0,10)/2

fig =  plt.figure()
ax = fig.add_subplot(111,projection='3d')
plt.scatter(X[:, 0],X[:, 1], X[:,2])
plt.show()


clf = KMeans(n_clusters=5)
clf.fit(X)

centroids = clf.cluster_centers_
labels = clf.labels_


plt.scatter(centroids[:, 0],centroids[:, 1],centroids[:,2], marker = "x", linewidths = 5, zorder = 20)
plt.show()