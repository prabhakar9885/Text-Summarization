
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

cdf.init( idf_file = "idf.out" )

clusters, clusters2 = p.load(open("./clusters.out", "rb"))
km.index, km.tokenAtIndex = p.load( open("./indexForCluster.out", "rb") )


sourceFile = sys.argv[1]
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

score_prev = [ 0 for i in xrange(len(clusters)) ]
score = [ 0 for i in xrange(len(clusters)) ]
# diff: Holds the difference between the previous score and the current score for each cluster
diff = [ 0 for i in xrange(len(clusters)) ]
# next_sentnc_in_cluster: Holds the index of the next statement from each cluster that must be considered for building sumary
next_sentnc_in_cluster = [ 0 for i in xrange(len(clusters)) ]


number_of_clusters = len(clusters)
i = 0
non_summary_vecs = []
while i < number_of_clusters:
	'''
	Initializes the score_prev, score, diff
	'''
	sentence = clusters2[i][ 0 ]
	sent_vec = seed_sentences_vecs[sentence]

	non_summary_vecs = []
	for s in seed_sentences_vecs:
		if s not in summary_vecs:
			non_summary_vecs.append( seed_sentences_vecs[s] )
	if sent_vec in non_summary_vecs:
		non_summary_vecs.remove(sent_vec)

	f_av = cdf.compute_score( summary_vecs, seed_sentences_vecs, sent_vec, clusters, lambdaVal = 1 )
	# print f_av
	f_a = cdf.compute_score( summary_vecs, seed_sentences_vecs, None, clusters, lambdaVal = 1 )
	# print f_a
	f_bv = cdf.compute_score( non_summary_vecs, seed_sentences_vecs, sent_vec, clusters, lambdaVal = 1 )
	# print f_bv
	f_b = cdf.compute_score( non_summary_vecs, seed_sentences_vecs, None, clusters, lambdaVal = 1 )
	# print f_b

	if f_av - f_a >= f_bv - f_b:
		#print "Add: " + str( f_av - f_a - (f_bv - f_b) )
		summary.append( sentence )
		summary_vecs.append( sent_vec )
		number_of_clusters = len(clusters)

	clusters[i].remove( sent_vec )
	clusters2[i].remove( sentence )
			
	j = 0
	while j < number_of_clusters:
		if len(clusters[j]) == 0:
			#print "skip"
			del clusters[j], clusters2[j]
			number_of_clusters = len(clusters)
		else:
			j += 1
	
	i += 1
	if i == number_of_clusters and number_of_clusters>0:
		i = 0
	elif number_of_clusters == 0:
		break


summaryAsText = ""
for i in summary:
	summaryAsText += i.strip();

print summaryAsText
print "Summary Info:"
print "%d lines of %d" % ( len(summary), len(seed_sentences) )
print "%d chars" %sum([ len(i) for i in summary ])
print( "Summary ratio: %.2f" %  (100.0*len(summaryAsText)/len(sentences)) )
