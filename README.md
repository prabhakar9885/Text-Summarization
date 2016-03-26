# Text Summarizer

### How to run the code?
- Generate ``idf.out`` file for the docs in ``TEST_docs_Parsed`` directory

  ```sh
   $ python calculate_idf.py ../TEST_docs_Parsed/
   ```
-  Using ``k-means`` generate ``clusters`` for a sample file from ``TEST_docs_Parsed`` directory

   ```sh
    $ python k_means.py ../TEST_docs_Parsed/d30001t/C1 3
   ```
- Generate summary for the same doc for which clustering is done in previous step

   ```sh
    $ python Generate_Summary.py ../TEST_docs_Parsed/d30001t/C1
   ```

For more information check [README.pdf]


### Assumptions made:
- In page 7, equation(6), alpha is taken as 1