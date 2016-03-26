
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
while i < number_of_clusters:
	'''
	Initializes the score_prev, score, diff
	'''
	sentence = clusters2[i][ next_sentnc_in_cluster[i] ]	
	sent_vec = seed_sentences_vecs[sentence]
	score_prev[i] = score[i]
	score[i] = cdf.compute_score( summary_vecs, seed_sentences_vecs, sent_vec, clusters, lambdaVal = 1 )
	diff[i] = score[i] - score_prev[i]

	next_sentnc_in_cluster[i] += 1
	if next_sentnc_in_cluster[i] == len(clusters[i]):
		del clusters[i], clusters2[i], next_sentnc_in_cluster[i]
		number_of_clusters = len(clusters)
		continue
	else:
		i += 1

	if sum( [ len(cluster) for cluster in clusters ] ) == 0:
		break

# targetIndex: Holds the index of the statement that must go into the summary
targetIndex = 0;

while targetIndex < number_of_clusters:
	'''
	Performs the summarization task using sub-modular function
	'''
	for i in xrange( 1, len(clusters) ):
		if diff[targetIndex] < diff[i]:
			targetIndex = i

	summary.append( clusters2[targetIndex][next_sentnc_in_cluster[targetIndex]] )
	next_sentnc_in_cluster[targetIndex] += 1

	if next_sentnc_in_cluster[targetIndex] == len(clusters2[targetIndex]):
		del clusters[targetIndex], clusters2[targetIndex], next_sentnc_in_cluster[targetIndex]
		targetIndex = 0;
		number_of_clusters = len(clusters)
	else:
		i = targetIndex
		sentence = clusters2[i][ next_sentnc_in_cluster[i] ]	
		sent_vec = seed_sentences_vecs[sentence]
		score_prev[i] = score[i]
		score[i] = cdf.compute_score( summary_vecs, seed_sentences_vecs, sent_vec, clusters, lambdaVal = 1 )
		diff[i] = score[i] - score_prev[i]
		targetIndex = 0
		continue

	if sum( [ len(cluster) for cluster in clusters ] ) == 0:
		break

summaryAsText = ""
for i in summary:
	summaryAsText += i.strip();

print summaryAsText
print "Summary Info:"
print "%d lines of %d" % ( len(summary), len(seed_sentences) )
print "%d chars" %sum([ len(i) for i in summary ])
print( "Summary ratio: %.2f" %  (100.0*len(summaryAsText)/len(sentences)) )
