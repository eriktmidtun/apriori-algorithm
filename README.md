# Apriori-algorithm
A python program to read a `.csv` file with transactions and finds the frequent itemsets and association rules.

## Usage
Clone the repository

Make a file called `apriori.csv` in the same folder, and copy in the transactions. You can test the example csv file. Just remove the `.example` extension.

Run the script with python:

```bash
python apriori.py #min_support_count:<int> #min_confidence_threshold:<float>
```

or

```bash
./apriori.py #min_support_count:<int> #min_confidence_threshold:<float>
```


The filename for the .csv can be changed in the code

After running the script you can choose a itemset to genereate a table for 

```text
Print association rules table for a itemset? format = A,B,C
C,H,I

Minimum confidence threshold: 0.6

 Candidate    Candidate      Support    Confidence  Accepted?
-----------  -----------  ---------  ------------  -----------
I            C,H                  4      0.5       No
C,I          H                    3      0.666667  Yes
H,I          C                    2      1         Yes
C            H,I                  3      0.666667  Yes
C,H          I                    2      1         Yes
H            C,I                  4      0.5       No 

------Accepted Association rules-------
{H,I} => {C}    {C,H} => {I}    {C,I} => {H}    {C} => {H,I}
```