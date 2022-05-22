import csv
import sys
from tabulate import tabulate
from typing import Tuple, List, Dict, FrozenSet
from colorama import init, Back, Fore
from itertools import permutations


def read_from_file(filename="apriori.csv") -> Tuple[List[List[str]], List[str]]:
    rows = []
    header = []
    with open(filename, 'r') as file:
        csvreader = csv.reader(file)
        header = next(csvreader)
        for row in csvreader:
            rows.append(row)
    return rows, header

def row_to_mapped_transactions(rows: List[List[str]]) -> Dict[str, List[str]]:
    mapped_transactions = {}
    for row in rows:
        id: str = row[0]
        mapped_transactions[id] = row[1:]
    return mapped_transactions
        
def check_for_multiple_equal_items(rows: List[List[str]]) -> bool:
    all_unique = True
    for i, row in enumerate(rows):
        if(len(set(row)) != len(row)):
            print(f"row {i} has multiple items of the same type")
            all_unique = False
    return all_unique


def get_support_counts_init(rows: List[List[str]]) -> Dict[FrozenSet[str], int]:
    support_counts = {}
    for row in rows:
        for item in row:
            key = frozenset(item)
            support_counts[key] = support_counts.get(key, 0) + 1
    return dict(sorted(support_counts.items(), key=lambda item: row_to_string(item[0])))

def get_support_counts2(transactions: Dict[str, List[str]], itemsets) :
    support_counts_dict = {}
    for itemset in itemsets:
        key = frozenset(itemset)
        support_counts_dict[key] = 0
    for items in transactions.values():
        for itemset in itemsets:
            if itemset.issubset(set(items)):
                key = frozenset(itemset)
                support_counts_dict[key] = support_counts_dict.get(key) + 1
    return dict(sorted(support_counts_dict.items(), key=lambda item: row_to_string(item[0])))

def row_to_string(row)-> str:
    return ",".join(sorted(list(row)))

def prune_itemsets(min_support:int, support_counts: Dict[List[str], int]) ->  Dict[List[str], int]:
    new_support_counts = {}
    for itemset, support in support_counts.items():
        if support >= min_support:
            new_support_counts[itemset] = support
    return new_support_counts

def color_by_support(min_support: int, value: int) -> str:
    if value < min_support:
        return f"{Back.RED}{Fore.BLACK}{value}{Back.RESET}{Fore.RESET}"
    return f"{value}"

def generate_table(min_support, support_counts, headers=["Itemset", "Support"]):
    table_with_pruning = []
    for itemset, support in support_counts.items():
        table_with_pruning.append([row_to_string(itemset), color_by_support(min_support, support)])
    print("\n",tabulate(table_with_pruning, headers, tablefmt="pretty"),"\n")

def generate_itemsets(itemsets: List[str], size: int) -> List[List[str]]:
    new_itemsets = set()
    for i in range(len(itemsets)):
        for j in range(i+1, len(itemsets)):
            new_itemset = itemsets[i].union(itemsets[j])
            if len(new_itemset) == size:
                new_itemsets.add(new_itemset)
    return list(new_itemsets)

def get_max_transaction_count(transactions):
    max_count = 0
    for transaction in transactions.values():
        if len(transaction) > max_count:
            max_count = len(transaction)
    return max_count

def get_max_support_count(support_counts):
    if len(support_counts.keys()) > 0:
        return max(support_counts.values())
    return 0

def get_association_rules_candidates(itemset):
    rules = {}
    perms = list(permutations(itemset,len(itemset)))
    for perm in perms:
        for split in range(1,len(perm)):
            first_half = frozenset(perm[:split])
            secound_half = frozenset(perm[split:])
            if first_half in rules.keys():
                if secound_half not in rules[first_half]:
                    rules[first_half].append(secound_half)
            else:
                rules[first_half] = [secound_half]
    return rules

def print_association_rules(association_rules):
    for first, secound in association_rules.items():
        for version in secound:
            first_str = row_to_string(list(first))
            secound_str = row_to_string(list(version))
            print("{"+ first_str + "}" + " => " + "{" + secound_str + "}", end="\t")
    print()

def print_association_rules_table(itemset, all_support_counts, threshold):
    canidates = get_association_rules_candidates(frozenset(itemset))
    print(f"\nMinimum confidence threshold: {threshold}")
    table = []
    accepted_association_rules = []
    for (first, secound) in canidates.items():
        row = []
        for version in secound:
            first_str = row_to_string(list(first))
            row.append(first_str)
            secound_str = row_to_string(list(version))
            row.append(secound_str)
            row.append(str(all_support_counts[first]))
            confidence = all_support_counts[frozenset(itemset)] / all_support_counts[first]
            row.append(str(confidence))
            accepted = confidence >= threshold
            row.append("Yes" if accepted else "No")
            table.append(row)
            if accepted:
                accepted_association_rules.append(row[:2])
    print("\n",tabulate(table, headers=[
        "Candidate", "Candidate", "Support", "Confidence", "Accepted?"], tablefmt="pretty"),"\n")
    print("\n------Accepted Association rules-------")
    for rule in accepted_association_rules:
        print("{"+ rule[0] + "}" + " => " + "{" + rule[1] + "}", end="\t")
    print("")
    

def main():
    argv = sys.argv
    if len(argv) < 3: return
        
    min_support: int = int(argv[1])

    min_threshold: float = float(argv[2])
    

    print("---------APRIORI----------")
    print(f"\nMinimum support count: {min_support}")
    print(f"\nMinimum confidence threshold: {min_threshold}")
    

    rows, headers = read_from_file()
    transactions = row_to_mapped_transactions(rows);

    max_iterations = get_max_transaction_count(transactions)
    print(f"\nMaximum iterations: {max_iterations}\n")

    init() # initilize colors in print output
    table = [(k, row_to_string(v)) for k, v in transactions.items()]
    print(tabulate(table, headers, tablefmt="pretty"))
    
    support_counts = get_support_counts_init(transactions.values())
    
    all_itemsets = []
    all_frequent_itemsets = []
    all_frequent_support_counts = {}
    i=2
    while max_iterations >= i:
        generate_table(min_support, support_counts)

        if get_max_support_count(support_counts) < min_support:
            break

        frequent_itemsets = prune_itemsets(min_support, support_counts)
        
        all_itemsets.append(list(support_counts.keys()))
        all_frequent_itemsets.append(list(frequent_itemsets.keys()))
        all_frequent_support_counts.update(frequent_itemsets)

        itemsets = generate_itemsets(list(frequent_itemsets.keys()), i)

        support_counts = get_support_counts2(transactions, itemsets)
        i += 1
    
    print("All frequent itemsets")
    all_frequent_itemsets_flattened = [item for sublist in all_frequent_itemsets for item in sublist]
    for idx, frequent_itemset in enumerate(all_frequent_itemsets_flattened):
        if len(frequent_itemset) > 1:
            association_rules_candidates = get_association_rules_candidates(all_frequent_itemsets_flattened[idx])
            
            print("{" + row_to_string(frequent_itemset) + "}" + " : ", end=" ")
            print_association_rules(association_rules_candidates)
        else:
            print("{" + row_to_string(frequent_itemset) + "}")

    print("\nPrint association rules table for a itemset? format = A,B,C")
    print_rule_table_for_itemset = input()
    chosen_itemset = frozenset(print_rule_table_for_itemset.split(","))
    if chosen_itemset not in all_frequent_itemsets_flattened:
        print("Invalid input")
    print_association_rules_table(chosen_itemset, all_frequent_support_counts, min_threshold)

        
if __name__ == "__main__":
    main()