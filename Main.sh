###########################################################################
#
# Usage:
# ======
# bash Main.sh <path to folder containing the docs that are to be summarized> 
#				<Clustering-Algorithm>
# 				<No. of Clusters> 
#	Clustering-Algorithm: 	1 -> k-means; 2-> Chinese Whispers ; 3-> Hierarchical Clustering
#	No. of clusters: 		Required for k-means and Hierarchical Clustering
#
# eg.,	bash Main.sh ../IRE/Project/TEST_docs_Parsed/d30001t/ 1 3
# eg.,	bash Main.sh ../IRE/Project/TEST_docs_Parsed/d30001t/ 2 
# eg.,	bash Main.sh ../IRE/Project/TEST_docs_Parsed/d30001t/ 3 3
#
###########################################################################


#!/bin/bash

dirName="$1"
clusteringAlgo="$2"
clustersCount=-1
if [[ $clusteringAlgo -ne "2" ]]; then
	clustersCount="$3"
fi
summarySize=655

if [[ -d "$dirName" ]]; then
	echo -n "Generating tf-idf scores..."
	python calculate_idf.py "$dirName" > /dev/null
	echo "done"
	echo -n "Generating Clusters..."
	python clustering.py "$dirName" "$clusteringAlgo" "$clustersCount"> /dev/null
	echo "done"
	echo -n "Generating Summary..."
	python Generate_Summary.py "$dirName"
	echo "done"
else
	echo "Director not found: $dirName"
fi
