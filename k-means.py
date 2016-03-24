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
	for i in xrange(len(vec1)):
		numer += (vec1[i]*vec2[i]*idf.values()[i]*idf.values()[i])
		denom1 += (vec1[i]*vec1[i]*idf.values()[i]*idf.values()[i])
		denom2 += (vec2[i]*vec2[i]*idf.values()[i]*idf.values()[i])
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
		temp = [0.0] * len(index)
		for token in tokens:
			temp[index[token]] += 1
		docvec.append(temp)
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
			centroids.append(docvec[r])
	while iterations != 2:
		print iterations
		iterations += 1
		for vec in docvec:
			print vec
			maxd = -1.0
			cent = 0
			for i in xrange(k):
				dist = calculate_similarity(vec, centroids[i], idf)
				print dist
				if dist > maxd:
					maxd = dist
					cent = i
			clusters[cent].append(vec)

		for i in xrange(k):
			print i
			print '--'
			temp = [0] * len(index)
			for member in clusters[i]:
				temp = map(add, temp, member)
			myint = float(len(clusters[i]))
			
			if myint!= 0:
				temp = [x/myint for x in temp]	
				for j in xrange(len(centroids[i])):
					centroids[i][j] = temp[j]
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
