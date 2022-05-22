# Apriori-algorithm
A python program to read a csv file with transactions and finds the frequent itemsets.

## Usage
Clone repository

Make a file called apriori in the same folder. You can test the example csv file. Just remove the .example extension.

run the script with

```bash
python apriori.py #min_support_count: int #min_confidence_threshold: float
```

The filename can be changed in the code

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