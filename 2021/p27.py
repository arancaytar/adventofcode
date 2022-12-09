from collections import Counter
from functools import reduce
import sys

def get_pairs(word):
    return Counter(zip(word[:-1], word[1:])), [(word[0], word[1]), (word[-2], word[-1])]

def step(pair_counts, end_pieces, rules):
    new_counts = Counter()
    for (a, b), j in pair_counts.items():
        if (a, b) in rules:
            c = rules[a, b]
            new_counts[(a, c)] += j
            new_counts[(c, b)] += j
        else:
            new_counts[a, b] += j
    if end_pieces[0] in rules:
       end_pieces[0] = end_pieces[0][0], rules[end_pieces[0]]
    if end_pieces[1] in rules:
       end_pieces[1] = rules[end_pieces[1]], end_pieces[1][1]
    return new_counts, end_pieces

def analyse(pair_counts, end_pieces) -> Counter:
    elements = Counter()
    for (a, b), i in pair_counts.items():
        elements[a] += i
        elements[b] += i
    for i, j in elements.items():
        elements[i] = j // 2
    elements[end_pieces[0][0]] += 1
    elements[end_pieces[1][1]] += 1
    return elements

def solve(start: str, rules: dict, k: int):
    pairs, end_pieces = get_pairs(start)
    for i in range(k):
        pairs, end_pieces = step(pairs, end_pieces, rules)
    counts = analyse(pairs, end_pieces)
    s = sorted(counts.keys(), key=lambda i: counts[i])
    return counts[s[-1]] - counts[s[0]]

def read() -> (str, dict):
    text = sys.stdin.read().split()
    start = text[0]
    rules = {}
    for i in range(1, len(text), 3):
        rules[tuple(text[i])] = text[i+2]
    return start, rules

start, rules = read()
print(solve(start, rules, 10))
