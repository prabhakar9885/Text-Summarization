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

- **Compute ROUG Score**:
  ```sh
   $ java -cp C_Rouge/C_ROUGE7.jar executiverouge.C_ROUGE7 SysGeneratedSummary.txt  TestData/Test_Summaries/d30001t  1 A R
   ```
   Refer [ROUG Score computation](./C_Rouge/ReadMe)

- [Git page](http://prabhakar9885.github.io/Text-Summarization/)
- [Youtube](https://www.youtube.com/playlist?list=PLtBx4kn8YjxJUGsszlev52fC1Jn07HkUw)
   


### Assumptions made:
- For more information refer [A class of submodular functions for document summarization](http://dl.acm.org/citation.cfm?id=2002537)
- In page 7, equation(6), alpha is taken as 1
