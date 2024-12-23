from grid import Grid
from graph import dijkstra,DGraph
import sys
import numpy as np
from collections import Counter, deque
from itertools import islice

def read():
    return (list(map(int, sys.stdin.read().strip().split())),)

def next_number(n):
    n = (n ^ (n << 6)) & 0xffffff
    n = (n ^ (n >> 5))
    return (n ^ (n << 11)) & 0xffffff

def solve1(numbers):
    def get_i(start, n):
        for i in range(n):
            start = next_number(start)
        return start
    return sum(get_i(x, 2000) for x in numbers)

def solve2(numbers):
    def yield_last_digit(start, n):
        for i in range(n):
            start = next_number(start)
            yield start % 10
    def yield_diffs(start, n):
        x = start % 10
        for y in yield_last_digit(start, n):
            yield y, y-x
            x = y

    score = Counter()
    for x in numbers:
        seen = {}
        b = c = d = None
        for next_digit, next_diff in yield_diffs(x, 2000):
            a, b, c, d = b, c, d, next_diff
            if (a,b,c,d) not in seen:
                score[a,b,c,d] += next_digit
                seen[a,b,c,d] = next_digit
    return max(score.values())

def main():
    problem = read()
    print(f"Problem 1: {solve1(*problem)}")
    print(f"Problem 2: {solve2(*problem)}")

main()