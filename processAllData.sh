#!/bin/bash

inputFolder="../TEST_docs_Parsed/"
humanSummary="../Test_Summaries/"
dirlist=($(ls -1 "$inputFolder"))
algo=3

for dir in ${dirlist[*]}
do
	echo "Processing "$dir
	dirName="$inputFolder$dir"
	bash Main.sh "$dirName" $algo 3
	echo "----------------------------------------"
	summaryFile="$dirName.summary"
	humanSummaryFile="$humanSummary$dir"
	echo $summaryFile
	echo $humanSummaryFile
	java -cp ./C_Rouge/C_ROUGE7.jar executiverouge.C_ROUGE7 "$summaryFile"  "$humanSummaryFile"  1 A R >> ROUG1.3
	rm *.out
done