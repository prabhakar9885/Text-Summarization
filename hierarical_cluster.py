"""
Demo of Hierarical Clustering algorithm
"""

import numpy as np
from matplotlib import pyplot as plt
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster
from nltk import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
import string
from stemming.porter2 import stem
import random
from operator import add
import pickle as p
import sys, os

index = {}			# Stores the index of term in the idf list
tokenAtIndex = {}	# Stores the mapping of the index->term w.r.t the idf list
sentindex = {}		# Stores the mapping sentence->index

def getfiles(directory):
	files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
	for i in xrange(len(files)):
		files[i] = os.path.join(directory , files[i])
	return files



def Create_Hierarical_Clusters( docvec, cluster_count ):

	X = docvec

	# Clustering process starts
	Z = linkage(X, 'ward')
	clusters = fcluster( Z, 3, criterion='maxclust') # Clustering criteria: Max_Num_of_clusters=3

	# Visualize the clusters
	# plt.scatter(X[:,0], X[:,1], c=clusters, cmap='prism')  # plot points with cluster dependent colors
	# plt.show()

	dendrogram(
	    Z,
	    truncate_mode='lastp',  # show only the last p merged clusters
	    show_leaf_counts=False,  # otherwise numbers in brackets are counts
	    leaf_rotation=90.,
	    leaf_font_size=12.,
	    show_contracted=False,  # to get a distribution impression in truncated branches
	)
	plt.show()

	# Store each cluster as an element of a dictionary.
	clusters_collection = {}
	for index in xrange( len(clusters) ):
		cluster_no = clusters[index]
		if cluster_no in clusters_collection:
			clusters_collection[cluster_no].append( X[index] )
		else:
			clusters_collection[cluster_no] = [ X[index] ]

	return clusters_collection


def createvec(source, isFileOrDir=True):
	global index
	doc = []
	docvec = []
	sourceIsFileOrDir = True
	
	if isFileOrDir:
		if os.path.isdir(source):
			# Source is a directory => Create Docvector for all the sentences present in the docs under that directory
			files = getfiles(source)
		elif os.path.isfile(source):
			# Source is a file => Create DocVector for all the sentences present in the file
			files = [source]
	else:
		# Consider the value of Source for creating the DocVec
		sourceIsFileOrDir = False
		read_doc = sent_tokenize(source)
		doc += read_doc
	
	if sourceIsFileOrDir:
		for f in files:
			read_doc = ""
			fp = open(f, 'r')
			read_doc = fp.read()
			read_doc = sent_tokenize(read_doc)
			doc += read_doc
	
	for i in xrange(len(doc)):
		sentindex[i] = doc[i]
		sent = doc[i]
		tokens = word_tokenize(sent)
		stops = stopwords.words('english')
		tokens = [token for token in tokens if token not in set(string.punctuation) and token not in stops]
		for j in xrange(len(tokens)):
			tokens[j] = stem(tokens[j])
		temp = {}
		for token in tokens:
			if index[token] in temp:
				temp[index[token]] += 1.0
			else:
				temp[index[token]] = 1.0
		docvec.append(dict(temp))
	return docvec


def expand_docvec(docvec):
	vecs = []
	dim = np.max( [ np.max(i.keys()) for i in docvec ] )

	for vec in docvec:
		l=[ 0 for i in range(dim+1) ]
		for i in vec:
			l[i] = vec[i]
		vecs.append(l)

	vecs_1 = [ np.array(i) for i in vecs ]
	vecs = np.array( vecs_1 )
	del vecs_1

	return vecs


def contract_docvec(docvec):
	final_vec = []
	for vec in docvec:
		d = {}
		for i in xrange(len(vec)):
			if vec[i]!=0:
				d[i] = vec[i]
		final_vec.append( d )
	return final_vec


def normalize_clusters(clusters):
	clusters_new = []
	for key in clusters:
		cluster = clusters[key]
		clusters_new.append( contract_docvec(cluster) )
	return clusters_new



def main(source, k):
	idf = p.load( open("idf.out", "rb+") )
	idx = 0
	indexFile = "indexForCluster.out"
	clustersFile = "clusters.out"

	for term in idf:
		index[term] = idx
		tokenAtIndex[idx] = term
		idx += 1
	p.dump( (index, tokenAtIndex), open(indexFile, "wb+") )
	docvec = createvec(source)

	docvec_expanded = expand_docvec(docvec)
	clusters_expanded = Create_Hierarical_Clusters( docvec_expanded, k)
	clusters = normalize_clusters( clusters_expanded )

	p.dump( (clusters,[]) , open(clustersFile, "wb+") )


if __name__ == "__main__":
	main( sys.argv[1], int(sys.argv[2]) )
