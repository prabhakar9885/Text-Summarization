###########################################################################
#
# Usage:
# ======
# bash Main.sh <path to folder containing the docs that are to be summarized> <No. of Clusters> <Summary size in words>
#
# eg.,	bash Main.sh ../IRE/Project/TEST_docs_Parsed/d30001t/ 3 300
#
###########################################################################


#!/bin/bash

dirName="$1"
clusteringAlgo="$2"
summarySize=655

if [[ -d "$dirName" ]]; then
	echo -n "Generating tf-idf scores..."
	python calculate_idf.py "$dirName" > /dev/null
	echo "done"
	echo -n "Generating Clusters..."
	python clustering.py "$dirName" "$clusteringAlgo" > /dev/null
	echo "done"
	echo -n "Generating Summary..."
	python Generate_Summary.py "$dirName"
	echo "done"
else
	echo "Director not found: $dirName"
fi
