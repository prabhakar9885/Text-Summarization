import os
from nltk import word_tokenize
from nltk.corpus import stopwords
import string
from stemming.porter2 import stem
from math import log10

idf = {}
docs = 0

def getfiles(curdir):
	dirs = [f for f in os.listdir(curdir)]
	for direc in dirs:
		curpath = os.path.join(curdir, direc)
		files = [f for f in os.listdir(curpath) if os.path.isfile(os.path.join(curpath, f))]
		for i in xrange(len(files)):
			files[i] = os.path.join(curpath , files[i])
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
	curdir = './IRE_project/TEST_docs_Parsed/'
	getfiles(curdir)
	print docs
	for term in idf:
		idf[term] = log10(float(docs)/(1.0 + float(idf[term])))
	print idf

	
main()
