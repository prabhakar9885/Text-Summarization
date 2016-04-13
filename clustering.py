"""
Given the path for a specific directory in curfile variable, it gives k clusters of sentences.
clusters contains cluster of sentences in vector(dict) from
while clusters2 contains cluster of sentences in original form

Usage: python k_means.py <path-to-directory-of-docs> <number-of-clusters>

"""
from nltk import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
import string
from stemming.porter2 import stem
import random
from operator import add
import pickle as p
import sys, os
import graph_builder
import cw
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster
import numpy as np
from matplotlib import pyplot as plt

index = {}			# Stores the index of term in the idf list
tokenAtIndex = {}	# Stores the mapping of the index->term w.r.t the idf list
sentindex = {}		# Stores the mapping sentence->index
vecindex = {}

def getword(idx):
	for key, value in index.iteritems():
		if value == idx:
			return key

def calculate_similarity(vec1, vec2, idf, tokenAtIndex):
	numer = 0.0
	denom1 = 0.0
	denom2 = 0.0 
	for key in vec1:
		word = tokenAtIndex[key]
		if key in vec2:
			numer += (vec1[key]*vec2[key]*idf[word]*idf[word])
		denom1 += (vec1[key]*vec1[key]*idf[word]*idf[word])

	for key in vec2:
		word = tokenAtIndex[key]	
		denom2 += (vec2[key]*vec2[key]*idf[word]*idf[word])
	
	denom1 = denom1**0.5
	denom2 = denom2**0.5
	return numer/(denom1*denom2)

def getfiles(directory):
	files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
	for i in xrange(len(files)):
		files[i] = os.path.join(directory , files[i])
	return files

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
		vecindex[i] = dict(temp)
	return docvec

def kmeans(docvec, k, idf):
	centroids = []
	
	randints = []
	iterations = 0
	while len(centroids) != k:
		r = random.randint(0,len(docvec)-1)
		if docvec[r] not in centroids:
			centroids.append(dict(docvec[r]))
	
	while iterations != 100:
		iterations += 1
		idx = 0
		clusters = []	# Stores the vectors 
		clusters2 = []	# Stores the index of the vectors w.r.t docvec
		for j in xrange(k):
			clusters.append([])
			clusters2.append([])
		for vec in docvec:
			maxd = -1.0
			cent = 0
			for i in xrange(k):
				sim = calculate_similarity(vec, centroids[i], idf, tokenAtIndex)
				if sim > maxd:
					maxd = sim
					cent = i
			clusters[cent].append(dict(vec))
			clusters2[cent].append(idx)
			idx += 1

		for i in xrange(k):
			temp = {}
			for member in clusters[i]:
				for key in member:
					if key in temp:
						temp[key] += 1
					else:
						temp[key] = 1
			myint = float(len(clusters[i]))
			
			if myint!= 0:
				for key in temp:
					temp[key] = temp[key]/myint	
				centroids[i] = dict(temp)
	return clusters, clusters2


def Create_Hierarical_Clusters( docvec, cluster_count ):

	X = docvec

	# Clustering process starts
	Z = linkage(X, 'ward')
	clusters = fcluster( Z, 3, criterion='maxclust') # Clustering criteria: Max_Num_of_clusters=3

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



def main(source, number, cluster_count):
	print number
	print cluster_count
	idf = p.load( open("idf.out", "rb+") )
	idx = 0
	indexFile = "indexForCluster.out"
	clustersFile = "clusters.out"

	for term in idf:
		index[term] = idx
		tokenAtIndex[idx] = term
		idx += 1
	docvec = createvec(source)
	p.dump( (docvec, index, tokenAtIndex, sentindex, vecindex), open(indexFile, "wb+") )

	if number == 1:
		k = cluster_count
		clusters, clusters2 = kmeans(docvec, k, idf)
		for i in xrange(k):
			for j in xrange(len(clusters2[i])):
				clusters2[i][j] = sentindex[clusters2[i][j]]

	elif number == 2:
		graph_builder.build(vecindex, idf, tokenAtIndex)
		clusters = cw.main()
		clusters2 = {}

	elif number == 3:
		k = cluster_count
		docvec_expanded = expand_docvec(docvec)
		clusters_expanded = Create_Hierarical_Clusters( docvec_expanded, k)
		clusters = normalize_clusters( clusters_expanded )
		clusters2 = {}
	
	p.dump( (clusters, clusters2) , open(clustersFile, "wb+") )
#print clusters2


if __name__ == "__main__":
	main( sys.argv[1], int(sys.argv[2]), int(sys.argv[3]) )
