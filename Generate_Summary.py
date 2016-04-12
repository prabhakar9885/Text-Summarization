"""
Generates summary of given documents such that the summary of the documents will be slightly more than W words.

Usage:
======
python Generate_Summary <path to the directory containing the documents> [<Size of summary in terms of words>]

e.g., python Generate_Summary ../asfs 
"""

print "Loading libs..."

import Coverage_And_Diversity_Functions as cdf
import pickle as p
from nltk import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from stemming.porter2 import stem
import sys, os, time
import clustering as km

print "Loading data..."

def getfiles(directory):
	files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
	for i in xrange(len(files)):
		files[i] = os.path.join(directory , files[i])
	return files


if len( sys.argv ) != 3 and len( sys.argv ) != 2:
	print "Error: Args Error"
	sys.exit(1)


cdf.init( idf_file = "idf.out" )

clusters, clusters2 = p.load(open("./clusters.out", "rb"))
km.docvec, km.index, km.tokenAtIndex, km.sentindex, km.vecindex = p.load( open("./indexForCluster.out", "rb") )


sourceFolder = sys.argv[1]
sourceFiles = getfiles(sourceFolder)

summary_size_in_bytes = 655
if len( sys.argv ) == 3:
	summary_size_in_bytes = int(sys.argv[2])
print "Max. summary size: %d bytes" %summary_size_in_bytes



# Extract sentences from each file in the sourceFolder and add them to seed_sentences
seed_sentences = []
for sourceFile in sourceFiles:
	sentences = open( sourceFile, "r" ).read()
	sentences = sent_tokenize(sentences)
	seed_sentences.extend( [sentence for sentence in sentences if sentence not in seed_sentences] )


# Build Sentence vector for each sentence and add them to seed_sentences_vecs.
seed_sentences_vecs = {}
all_sentence_vecs_without_v = []
shortest_sent_size = -1
for sentence in seed_sentences:
	seed_sentences_vecs[sentence] = km.createvec(sentence, isFileOrDir=False)[0]
	all_sentence_vecs_without_v.append( seed_sentences_vecs[sentence] )
	byte_count = len(sentence.strip())
	if seed_sentences_vecs[sentence] == -1:
		shortest_sent_size = byte_count
	elif shortest_sent_size > byte_count:
		shortest_sent_size = byte_count


current_sent_indx = 0
count_of_bytes_in_summary = 0
non_summary_vecs = []
summary = []
summary_vecs = []


print "Generating Summary"
st = time.time()



while count_of_bytes_in_summary + shortest_sent_size <= summary_size_in_bytes and len(seed_sentences) != 0:

	print "Summary till now: %d bytes" % count_of_bytes_in_summary
	print( "Processing sentences: " )
	max_profit_at_indx = 0
	max_profit_till_now = -1
	number_of_seed_sentences_vecs = len(seed_sentences_vecs)
	print "Total number of statements: %d" % ( number_of_seed_sentences_vecs )

	for i in xrange( number_of_seed_sentences_vecs ):
		sent = seed_sentences[i]
		v = seed_sentences_vecs[ sent ]
		all_sentence_vecs_without_v.remove( v )

		f_av = cdf.compute_score( summary_vecs, seed_sentences_vecs, v, \
																			clusters, km.tokenAtIndex, lambdaVal = 1 )
		f_a = cdf.compute_score( summary_vecs, seed_sentences_vecs, None, 
																			clusters, km.tokenAtIndex, lambdaVal = 1 )
		all_sentence_vecs_without_v.append( v )

		if f_av - f_a >= 0 or max_profit_till_now == -1:
			profit = f_av - f_a;
			if profit > max_profit_till_now:
				max_profit_till_now = profit
				max_profit_at_indx = i

		# print( "Sentence Index: " + str(i) + "; Profit: " + str(max_profit_till_now) )

	sentence_with_max_profit = seed_sentences[max_profit_at_indx]
	count_of_bytes_in_summary += len(sentence_with_max_profit.strip())
				

	summary.append( sentence_with_max_profit )
	summary_vecs.append( seed_sentences_vecs[sentence_with_max_profit] )

	seed_sentences.remove( sentence_with_max_profit )
	del seed_sentences_vecs[ sentence_with_max_profit ]
	

et = time.time()
print "Run-time: %s" %(et-st)


summaryAsText = ""
for i in summary:
	summaryAsText += i.strip();

print "Summary"
print summaryAsText
print "Saving summary to " + sourceFolder

out_file = open( sourceFolder + ".summary", "w+" )
out_file.write(summaryAsText)
out_file.close()
