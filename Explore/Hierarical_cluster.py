"""
Demo of Hierarical Clustering algorithm
"""

import numpy as np
from matplotlib import pyplot as plt
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster

# Generate some sample data.
a = np.random.multivariate_normal([10, 2], [[4, 2], [2, 3]], size=[100,])
b = np.random.multivariate_normal([25, 5], [[5, 1], [2, 4]], size=[100,])
X = np.concatenate((a, b))



# Clustering process starts

Z = linkage(X)

clusters = fcluster( Z, 3, criterion='maxclust') # Clustering criteria: Max_Num_of_clusters=3

# Visualize the clusters
plt.scatter(X[:,0], X[:,1], c=clusters, cmap='prism')  # plot points with cluster dependent colors
plt.show()

# Store each cluster as an element of a dictionary.
clusters_collection = {}
for index in xrange( len(clusters) ):
	cluster_no = clusters[index]
	if cluster_no in clusters_collection:
		clusters_collection[cluster_no].append( X[index] )
	else:
		clusters_collection[cluster_no] = [ X[index] ]