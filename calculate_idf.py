"""
USAGE:
======
python calculate_idf.py <path to TEST_docs_Parsed> 

e.g: python calculate_idf.py ../IRE/Project/TEST_docs_Parsed/d30001t/

"""
import os
from nltk import word_tokenize
from nltk.corpus import stopwords
import string
from stemming.porter2 import stem
from math import log10
import sys
import pickle as p

idf = {}
docs = 0

def getfiles(curdir):
	files = [f for f in os.listdir(curdir) if os.path.isfile(os.path.join(curdir, f))]
	for i in xrange(len(files)):
		files[i] = os.path.join(curdir , files[i])
	initialize(files)

def initialize(files):
	global docs
	global idf
	for f in files:
		docs += 1
		fp = open(f, 'r')
		document = fp.read()
		document = word_tokenize(document)
		stops = stopwords.words('english')
		document = [token for token in document if token not in stops and token not in set(string.punctuation)]
		for i in xrange(len(document)):
			document[i] = stem(document[i])
		temp = []
		for token in document:
			if token not in temp:
				if token in idf:
					idf[token] += 1
				else:
					idf[token] = 1
				temp.append(token)

def main():
	curdir = sys.argv[1] 	# Path to the "TEST_docs_Parsed" directory
	idfFile = "idf.out"
	getfiles(curdir)
	print "Number of docs in directory:", docs
	for term in idf:
		idf[term] = log10(float(docs)/(1.0 + float(idf[term])))

	p.dump( idf, open(idfFile, "wb+") )
	
main()
