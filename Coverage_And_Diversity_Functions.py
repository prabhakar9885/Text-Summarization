
import pickle as p
import sys
import k_means as km
import math as m


idf = []


"""
Computes Eq.6. for finding the the overall similarity of summary set S to ground set V
Returns L(S) 
"""
def get_coverage_score( S, V ):
	
	L = 0
	global idf

	for i in V:
		for sj in S:
			L += km.calculate_similarity( V[i], sj, idf )

	return L




"""
Computes Eq.7. for finding the the reward that is to be given for the summary set S
Returns R(S) 
"""
def get_diversity_score( S, V, P ):
	
	R = 0
	N = len(V)
	global idf

	for k in xrange( len(P) ):
		r = 0;
		J = [ sent for sent in S if sent in P[k] ]
		for j in J:
			for i in V:
				r += km.calculate_similarity( V[i], j, idf )
		r /= N
		R += m.sqrt(r)

	return R



"""
Computs Eq.2. for finding the summary quality
Returns F(S)
"""
def compute_score( S, V, newSent, P, lambdaVal ):
	
	if newSent in S:
		return -1;

	S1 = []
	for sent_vec in S:
		S1.append(sent_vec)

	if newSent is not None:
		S1.append(newSent)

	return get_coverage_score( S1, V ) + lambdaVal * get_diversity_score( S1, V, P )


def init(idf_file):
	global idf
	idf = p.load( open(idf_file,"rb") )

