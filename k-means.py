"""
Given the path for a specific file in curfile variable, it gives k clusters of sentences.
Just run the code and it gives k number of clusters.
"""



from calculate_idf import getfiles
from nltk import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
import string
from stemming.porter2 import stem
import random
from operator import add

index = {}

def calculate_similarity(vec1, vec2, idf):
	numer = 0.0
	denom1 = 0.0
	denom2 = 0.0 
	
	for key in vec1:
		if key in vec2:
			numer += (vec1[key]*vec2[key]*idf.values()[key]*idf.values()[key])
		denom1 += (vec1[key]*vec1[key]*idf.values()[key]*idf.values()[key])
	
	for key in vec2:	
		denom2 += (vec2[key]*vec2[key]*idf.values()[key]*idf.values()[key])
	
	denom1 = denom1**0.5
	denom2 = denom2**0.5
	return numer/(denom1*denom2)  



def createvec(curfile):
	global index
	fp = open(curfile, 'r')
	doc = fp.read()
	doc = sent_tokenize(doc)
	docvec = []
	for i in xrange(len(doc)):
		sent = doc[i]
		tokens = word_tokenize(sent)
		stops = stopwords.words('english')
		tokens = [token for token in tokens if token not in set(string.punctuation) and token not in stops]
		for j in xrange(len(tokens)):
			tokens[j] = stem(tokens[j])
		temp = {}
		for token in tokens:
			if token in temp:
				temp[index[token]] += 1.0
			else:
				temp[index[token]] = 1.0
		docvec.append(dict(temp))
	return docvec

def kmeans(docvec, k, idf):
	centroids = []
	clusters = []
	for j in xrange(k):
		clusters.append([])
	randints = []
	iterations = 0
	while len(centroids) != k:
		r = random.randint(0,len(docvec)-1)
		if docvec[r] not in centroids:
			centroids.append(dict(docvec[r]))
	while iterations != 50:
		iterations += 1
		for vec in docvec:
			maxd = -1.0
			cent = 0
			for i in xrange(k):
				sim = calculate_similarity(vec, centroids[i], idf)
				if sim > maxd:
					maxd = sim
					cent = i
			clusters[cent].append(dict(vec))

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
	return clusters





def main():
	curdir = './IRE_project/TEST_docs_Parsed/'
	idf = getfiles(curdir)
	idx = 0
	for term in idf:
		index[term] = idx
		idx += 1
	curfile = './IRE_project/TEST_docs_Parsed/d30001t/C1'
	docvec = createvec(curfile)
	k = 4
	clusters = kmeans(docvec, k, idf)
	print clusters

main()
