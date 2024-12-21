import sys
import math
import numpy as np
from collections import Counter

def read():
    towels, targets = sys.stdin.read().strip().split("\n\n")
    
    towels = towels.split(", ")
    targets = targets.split("\n")
    return towels, targets
    

def solve1(towels, targets):
    towels = set(towels)
    def possible(target):
        achieved = {0}
        for i in range(len(target)):
            if any(target[prefix: i + 1] in towels for prefix in achieved):
                achieved.add(i + 1)
        return len(target) in achieved
    
    return sum(possible(target) for target in targets)
    
def solve2(towels, targets):
    towels = set(towels)
    def options(target):
        achieved = [1]
        for i in range(len(target)):
            achieved.append(sum(achieved[prefix] * (target[prefix:i + 1] in towels) for prefix in range(i + 1)))
        return achieved[-1]
    
    return sum(options(target) for target in targets)

def main():
    problem = read()
    #print(f"S: {sample2()}")
    print(f"Problem 1: {solve1(*problem)}")
    print(f"Problem 2: {solve2(*problem)}")


def debug():
    return None
    

main()
#debug()



 