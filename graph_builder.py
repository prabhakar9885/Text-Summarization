import os
import sys
import cPickle as pickle
import networkx as nx
import clustering as cs

def build(vecindex, idf, tokenAtIndex):
  print "Unpickling"
  idf = pickle.load( open("idf.out", "rb+") )
  docvec, index, tokenAtIndex, sentindex, vecindex = pickle.load(open("indexForCluster.out", "rb+"))
  print "Building graph"
  gr = nx.Graph()
  gr.add_nodes_from(vecindex)

  print "Adding edges"
  count=0
  count_edges=0

  edge_list=[]

  for i in vecindex:
    count+=1
#if count%500==0:
#     print count
    for j in vecindex:
      if i!=j:
        similarity = cs.calculate_similarity(vecindex[i], vecindex[j], idf, tokenAtIndex)
        if similarity==1.0:
          print i,j
        else:
          if similarity>0.05:
            weight=similarity
            edge_list.append((i,j,weight))

          
  gr.add_weighted_edges_from(edge_list)

  print "Number of nodes\t",gr.number_of_nodes()
  print "Number of edges\t",gr.number_of_edges()

  print "Saving to file"
  pickle.dump(edge_list,open("edges.p","wb"))
  nx.write_gpickle(gr,"test.gpickle")
