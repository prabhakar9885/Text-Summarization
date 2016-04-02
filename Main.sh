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
noOfClusters="$2"
summarySize="$3"

if [[ -d "$dirName" ]]; then
	echo -n "Generating tfid scores..."
	python calculate_idf.py "$dirName" > /dev/null
	echo "done"
	echo -n "Generating Clusters..."
	python k_means.py "$dirName" "$noOfClusters" > /dev/null
	echo "done"
	echo -n "Generating Clusters..."
	python Generate_Summary.py "$dirName" "$summarySize"> "$dirName.summary"
	echo "done"
else
	echo "Director not found: $dirName"
fi