from grid import Grid
from graph import dijkstra,DGraph
import sys
import numpy as np
from collections import Counter, deque
from itertools import islice

def read():
    lines = sys.stdin.read().strip().split("\n")
    return ([tuple(line.split("-")) for line in lines],)


def solve1(lines):
    adjacency = {x:set() for a,b in lines for x in (a,b)}
    nodes = sorted(adjacency.keys())
    for a,b in lines:
        adjacency[a].add(b)
        adjacency[b].add(a)

    cliques = set()
    for i, a in enumerate(nodes):
        if a[0] == 't':
            for b in adjacency[a]:
                c = adjacency[a] & adjacency[b]
                cliques |= {frozenset({a,b,cc}) for cc in c}


    return len(cliques)


def solve2(lines):
    adjacency = {x: set() for a, b in lines for x in (a, b)}
    nodes = sorted(adjacency.keys())
    for a, b in lines:
        adjacency[a].add(b)
        adjacency[b].add(a)

    cliques = set()
    for i, a in enumerate(nodes):
        for b in adjacency[a]:
            c = adjacency[a] & adjacency[b]
            cliques |= {tuple(sorted([a, b, cc])) for cc in c}

    for i in range(4, len(nodes)):
        new_cliques = set()
        for clique in cliques:
            extender = set.intersection(*(adjacency[x] for x in clique))
            new_cliques |= {tuple(sorted(clique + (e,))) for e in extender}
        if len(new_cliques):
            cliques = new_cliques
        else:
            return ",".join(min(cliques))

def main():
    problem = read()
    print(f"Problem 1: {solve1(*problem)}")
    print(f"Problem 2: {solve2(*problem)}")

main()