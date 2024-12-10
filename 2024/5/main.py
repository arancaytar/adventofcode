import sys
from functools import cmp_to_key


def read():
    rules, sequences = sys.stdin.read().split("\n\n")
    rules = [tuple(map(int, x.split("|"))) for x in rules.split("\n")]
    sequences = [list(map(int, sequence.split(","))) for sequence in sequences.split("\n")]
    return rules, sequences

def check_sequence(sequence, preceding):
    done = set()
    occur = set(sequence)
    #print(preceding)
    for x in sequence:
        if x in preceding and not (preceding[x] & occur) <= done:
            #print(f"{x} in {sequence} is not preceded by {(occur & preceding[x]) - done}")
            return False
        done.add(x)
    return True

def solve1(rules, sequences):
    preceding = {b:set() for a,b in rules}
    for a,b in rules:
        preceding[b].add(a)
    
    return sum(x[len(x)//2] for x in sequences if check_sequence(x, preceding))

def topsort(parents):
    print(parents)
    parents = {x:set(y) for x,y in parents.items()}
    nodes = set(parents.keys()) | set.union(*(p for x,p in parents.items()))
    sequence = []
    while nodes:
        roots = {x for x in nodes if x not in parents or len(parents[x]) == 0}
        if len(roots) == 0:
            raise ValueError("No roots")
        elif len(roots) > 1:
            raise ValueError("Multiple roots (ambiguous sort)")
        else:
            [root] = roots
            sequence.append(root)
            nodes.remove(root)
            for x,p in parents.items():
                p -= {root}
    return sequence

def solve2_bad(rules, sequences):
    result = 0
    for sequence in sequences:
        domain = set(sequence)
        rules = {(a,b) for a,b in rules if {a,b} <= domain}
        if not rules:
            continue
        preceding = {b:set() for a,b in rules}
        for a,b in rules:
            preceding[b].add(a)
        ts = topsort(preceding)
        if sequence == ts:
            continue
        print(sequence, ts)
        result += ts[len(ts)//2]
        
    return result

def sort_with_rules(sequence, rules):
    def cmp(a,b):
        if (a,b) in rules:
            return -1
        elif (b,a) in rules:
            return 1
        else:
            return 0
    return sorted(sequence, key=cmp_to_key(cmp))
    
def solve2(rules, sequences):
    rules = set(rules)
    result = 0
    for sequence in sequences:
        correct = sort_with_rules(sequence, rules)
        if correct != sequence:
            result += correct[len(correct)//2]
    return result
        
    
def main():
    problem = read()
    print(f"Problem 1: {solve1(*problem)}")
    print(f"Problem 2: {solve2(*problem)}")

def debug():
    return None
    

main()
#debug()