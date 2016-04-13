# Text Summarizer

### How to run the code?
- **Syntax**:
  ```sh
   $ bash Main.sh <directory-path>  <Clustering-Algorithm> <No. of Clusters> 
   ```
   - **directory-path**: The path to the directory that contains the documentes that are to be summarized
   - **Clustering-Algorithm**: ``1`` -> k-means; ``2``-> Chinese Whispers ; ``3``-> Hierarchical Clustering
   - **No. of clusters**: 		Required for k-means and Hierarchical Clustering

   e.g.,
  ```sh
   $ bash bash Main.sh ../TEST_docs_Parsed/d30001t/ 3 4
   ```

For more information check [README.pdf]


### Assumptions made:
- In page 7, equation(6), alpha is taken as 1




bash Main.sh ../TEST_docs_Parsed/d30024t 3
java -cp ../C_Rouge/C_ROUGE7.jar executiverouge.C_ROUGE7 "Byte based Summary/d30007t.summary"  ../Test_Summaries/d30007t/  1 A R
