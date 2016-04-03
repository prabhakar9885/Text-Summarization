"""
Generates summary of given documents such that the summary of the documents will be slightly more than W words.

Usage:
======
python Generate_Summary <path to the directory containing the documents> <Size of summary in terms of words>

e.g., python Generate_Summary ../asfs/ 100
"""


import Coverage_And_Diversity_Functions as cdf
import pickle as p
from nltk import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from stemming.porter2 import stem
import sys, os, threading
import k_means as km
import copy, time


def getfiles(directory):
	files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
	for i in xrange(len(files)):
		files[i] = os.path.join(directory , files[i])
	return files


class GetSentenceScore(threading.Thread):
	
	def __init__(self, threadName, start_index, end_index):
		threading.Thread.__init__(self)
		self.threadName = threadName;
		self.start_index = start_index
		self.end_index = end_index
		self.max_profit_at_indx = 0
		self.max_profit_till_now = -1


	def run(self):
		global seed_sentences_vecs, seed_sentences, all_sentence_vecs_without_v
		all_sentence_vecs_without_v_local = copy.deepcopy(all_sentence_vecs_without_v)

		for i in xrange( self.start_index, self.end_index ):
			sent = seed_sentences[i]
			v = seed_sentences_vecs[ sent ]
			all_sentence_vecs_without_v_local.remove( v )

			f_av = cdf.compute_score( summary_vecs, seed_sentences_vecs, v, \
																				clusters, lambdaVal = 1 )
			f_a = cdf.compute_score( summary_vecs, seed_sentences_vecs, None, 
																				clusters, lambdaVal = 1 )
			f_bv = cdf.compute_score( all_sentence_vecs_without_v_local, seed_sentences_vecs, v, 
																				clusters, lambdaVal = 1 )
			f_b = cdf.compute_score( all_sentence_vecs_without_v_local, seed_sentences_vecs, None, 
																				clusters, lambdaVal = 1 )
			all_sentence_vecs_without_v_local.append( v )

			if f_av - f_a >= f_bv - f_b or self.max_profit_till_now == -1:
				profit = f_av - f_a;
				if profit > self.max_profit_till_now:
					self.max_profit_till_now = profit
					self.max_profit_at_indx = i
			print( self.threadName + ": Sentence Index: " + str(i) + "; Profit: " +\
						 str(self.max_profit_till_now) )



if len( sys.argv ) != 3:
	print "Error: python Generate_Summary.py targetFile"
	sys.exit(1)

cdf.init( idf_file = "idf.out" )

clusters, clusters2 = p.load(open("./clusters.out", "rb"))
km.index, km.tokenAtIndex = p.load( open("./indexForCluster.out", "rb") )


sourceFolder = sys.argv[1]
summary_size_in_words = sys.argv[2]
sourceFiles = getfiles(sourceFolder)


# Extract sentences from each file in the sourceFolder and add them to seed_sentences
seed_sentences = []
for sourceFile in sourceFiles:
	sentences = open( sourceFile, "r" ).read()
	sentences = sent_tokenize(sentences)
	seed_sentences.extend( [sentence for sentence in sentences if sentence not in seed_sentences] )


# Build Sentence vector for each sentence and add them to seed_sentences_vecs.
seed_sentences_vecs = {}
all_sentence_vecs_without_v = []
for sentence in seed_sentences:
	seed_sentences_vecs[sentence] = km.createvec(sentence, isFileOrDir=False)[0]
	all_sentence_vecs_without_v.append( seed_sentences_vecs[sentence] )


current_sent_indx = 0
count_of_words_in_summary = 0
non_summary_vecs = []
summary = []
summary_vecs = []


print "Generating Summary..."
start_time = time.time()

while count_of_words_in_summary < summary_size_in_words and len(seed_sentences) != 0:

	print "Summary till now: %d" % count_of_words_in_summary
	print( "Processing sentences: " )

	number_of_seed_sentences_vecs = len(seed_sentences_vecs)
	sizeOfSentenceBlock = number_of_seed_sentences_vecs/4
	
	threads = []
	thread_for_block_1 = GetSentenceScore( "T0", 0, sizeOfSentenceBlock )
	thread_for_block_2 = GetSentenceScore( "T1", sizeOfSentenceBlock, sizeOfSentenceBlock*2 )
	thread_for_block_3 = GetSentenceScore( "T2", sizeOfSentenceBlock*2, sizeOfSentenceBlock*3)
	thread_for_block_4 = GetSentenceScore( "T3", sizeOfSentenceBlock*3, number_of_seed_sentences_vecs)
	
	threads.append(thread_for_block_1)
	threads.append(thread_for_block_2)
	threads.append(thread_for_block_3)
	threads.append(thread_for_block_4)
	
	for thread in threads:
		thread.start()

	for thread in threads:
		thread.join()

	index_with_max_score = []
	for thread in threads:
		index_with_max_score.append( (thread.max_profit_at_indx , thread.max_profit_till_now) )

	max_profit_at_indx = max( index_with_max_score, key=lambda item:item[1] ) [0]

	sentence_with_max_profit = seed_sentences[max_profit_at_indx]
	count_of_words_in_summary += \
				len( [ i for i in sentence_with_max_profit.split(" ") if len(i.strip())!=0 ] )

	summary.append( sentence_with_max_profit )
	summary_vecs.append( seed_sentences_vecs[sentence_with_max_profit] )
	
	seed_sentences.remove( sentence_with_max_profit )
	del seed_sentences_vecs[ sentence_with_max_profit ]

	break

end_time = start_time = time.time()

print "Time-elapsed: %s" % (end_time - start_time)
print summary

#
#	Save the summary to a file
#
# summaryAsText = ""
# for i in summary:
# 	summaryAsText += i.strip()+"\n";

# if sourceFolder[-1]=='/':
# 	sourceFolder = sourceFolder[:-1]
# sourceFolder = sourceFolder.split("/")[-1]

# out_file = open( sourceFolder + ".summary", "w+" )
# out_file.write(summaryAsText)
# out_file.close()