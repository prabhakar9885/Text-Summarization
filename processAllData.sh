#!/bin/bash

inputFolder="../TEST_docs_Parsed/"
humanSummary="../Test_Summaries/"
dirlist=($(ls -1 "$inputFolder"))
algoList=(1 2 3)

for algo in "${algoList[@]}"
do
	for dir in ${dirlist[*]}
	do
		echo "----------------------------------------"
		echo "Processing "$dir
		dirName="$inputFolder$dir"
		rougFileName="ROUG_"$algo
		bash Main.sh "$dirName" $algo 3
		summaryFile="$dirName.summary"
		humanSummaryFile="$humanSummary$dir"
		echo $summaryFile
		echo $humanSummaryFile
		echo "$rougFileName" 
		echo -en "\n"$dir" : " >> "$rougFileName"
		java -cp ./C_Rouge/C_ROUGE7.jar executiverouge.C_ROUGE7 "$summaryFile"  "$humanSummaryFile"  1 A R >> "$rougFileName"
		rm *.out
	done
done