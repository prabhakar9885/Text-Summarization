
import pickle as p
import sys
import clustering as km
import math as m


idf = []


"""
Computes Eq.6. for finding the the overall similarity of summary set S to ground set V
Returns L(S) 
"""
def get_coverage_score( S, V , tokenAtIndex):
	
	L = 0
	global idf

	for i in V:
		for sj in S:
			L += km.calculate_similarity( V[i], sj, idf, tokenAtIndex)

	return L




"""
Computes Eq.7. for finding the the reward that is to be given for the summary set S
Returns R(S) 
"""
def get_diversity_score( S, V, P , tokenAtIndex):
	
	R = 0
	N = len(V)
	global idf

	for k in xrange( len(P) ):
		r = 0;
		J = [ sent for sent in S if sent in P[k] ]
		for j in J:
			for i in V:
				r += km.calculate_similarity( V[i], j, idf, tokenAtIndex )
		r /= N
		R += m.sqrt(r)

	return R



"""
Computs Eq.2. for finding the summary quality
Returns F(S)
"""
def compute_score( S, V, newSent, P, tokenAtIndex, lambdaVal):
	
	# if newSent in S:
	# 	return -1;

	S1 = []
	for sent_vec in S:
		S1.append(sent_vec)

	if newSent is not None:
		S1.append(newSent)

	return get_coverage_score( S1, V , tokenAtIndex) + lambdaVal * get_diversity_score( S1, V, P , tokenAtIndex)


def init(idf_file):
	global idf
	idf = p.load( open(idf_file,"rb") )

