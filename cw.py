import os
import sys
import networkx as nx
import cPickle as pickle

def chinese_whispers(G,node_list):
  print "Running Chinese whispers algorithm"
  no_it= 10

  dict_classes={}

  #Init
  print "Initializing"
  count=0
  for i in node_list:
    dict_classes[i]=count
    count+=1

  nx.set_node_attributes(G, "class", dict_classes)
  print "Length of dict classes\t",len(dict_classes)

  print "Iterating"
  for i in xrange(no_it):
    #Iterate over all nodes

#print "Iteration\t",i
    cnt=0
    for nd in nx.nodes_iter(G):
      cnt+=1
#      if cnt%1000==0:
#       print cnt
      strength_dict={}
      #Find highest strength class
      for nbrs in nx.all_neighbors(G,nd):
        nbr_class=G.node[nbrs]["class"]
        
        if nbr_class in strength_dict:
          strength_dict[nbr_class] += G[nd][nbrs]["weight"]
        else:
          strength_dict[nbr_class] = G[nd][nbrs]["weight"]

      #Class propogation
      max_str=0
      propogated_class=G.node[nd]["class"]
      for cl in strength_dict:
        if strength_dict[cl] > max_str:
          max_str=strength_dict[cl]
          propogated_class=cl

      G.node[nd]["class"]=propogated_class

  print "Finding final node classes"
  final_classes={}
  for i in nx.nodes_iter(G):
    cl=G.node[i]["class"]
    if cl in final_classes:
      final_classes[cl].append(i)
    else:
      final_classes[cl]=[i]
  temp = []
  for i in final_classes:
	temp.append(final_classes[i])
  final_classes = list(temp)
  	

  print "Pickling Final classes"
  print "Number of Final classes", len(final_classes)
  print final_classes
#  for i in final_classes:
# 
  return final_classes

def main():
  print "Unpickling"
  G=nx.read_gpickle("test.gpickle")

  print "Number of nodes\t",G.number_of_nodes()
  print "Number of edges\t",G.number_of_edges()

  node_list=G.nodes()
  final_classes = chinese_whispers(G, node_list)
  return final_classes
