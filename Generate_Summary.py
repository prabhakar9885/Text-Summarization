
import Coverage_And_Diversity_Functions as cdf
import pickle as p
from nltk import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from stemming.porter2 import stem
import sys
import k_means as km


if len( sys.argv ) != 2:
	print "Error: python Generate_Summary.py targetFile"
	sys.exit(1)

sourceFile = sys.argv[1]

cdf.init( idf_file = "idf.out" )

clusters, clusters2 = p.load(open("./clusters.out", "rb"))
km.index, km.tokenAtIndex = p.load( open("./indexForCluster.out", "rb") )


sentences = open( sourceFile, "r" ).read()
seed_sentences = sent_tokenize(sentences)
seed_sentences_vecs = {}
score = -1
score_prev = -1
summary = []
summary_vecs = []

for sentence in seed_sentences:
	if sentence not in seed_sentences_vecs:
		seed_sentences_vecs[sentence] = km.createvec(sentence, False)[0]

for i in xrange( len(seed_sentences_vecs) ):
	sentence = seed_sentences[i]
	sent_vec = seed_sentences_vecs[sentence]
	score = cdf.compute_score( summary_vecs, seed_sentences_vecs, sent_vec, clusters, lambdaVal = 1 )
	if score_prev < score:
		score_prev =  score
		summary.append( sentence )
		summary_vecs.append( sent_vec )
