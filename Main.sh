###########################################################################
#
# Usage:
# ======
# bash Main.sh <path to folder containing the docs that are to be summarized> 
#
# eg.,	bash Main.sh ../IRE/Project/TEST_docs_Parsed/d30001t/
#
###########################################################################


#!/bin/bash

dirName="$1"
noOfClusters="$2"

if [[ -d "$dirName" ]]; then
	echo -n "Generating tfid scores..."
	python calculate_idf.py "$dirName" > /dev/null
	echo "done"
	echo -n "Generating Clusters..."
	python k_means.py "$dirName" "$noOfClusters" > /dev/null
	echo "done"
	echo -n "Generating Clusters..."
	python Generate_Summary.py "$dirName" > "$dirName.summary"
	echo "done"
else
	echo "Director not found: $dirName"
fi