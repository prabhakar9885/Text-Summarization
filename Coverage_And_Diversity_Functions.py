
import pickle as p
import sys
import k-means as km
import math as m

ifd_file = sys.argv[1]
idf = p.load( ifd_file )



"""
Computes Eq.6. for finding the the overall similarity of summary set S to ground set V
Returns L(S) 
"""
def get_coverage_score( S, V ):
	
	L = 0

	for i in V:
		for j in S:
			L += km.calculate_similarity( i, j )

	return L




"""
Computes Eq.7. for finding the the reward that is to be given for the summary set S
Returns R(S) 
"""
def get_diversity_score( S, V, P ):
	
	R = 0
	N = len(V)

	for k in xrange( len(P) ):
		r = 0;
		J = [ sent for sent in S if sent in P[k]  ]
		for j in J:
			for i in V:
				r += km.calculate_similarity( i, j, idf )
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
	S1.append(S)
	S1.append(newSent)

	return get_coverage_score( S1, V ) + lambdaVal * get_diversity_score( S1, V, P )