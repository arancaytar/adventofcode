from grid import Grid
from graph import dijkstra,DGraph
import sys
import numpy as np
from collections import defaultdict
from itertools import islice
import re

def read():
    schematics = sys.stdin.read().strip().split("\n\n")
    schematics = [Grid.read(schematic, {'.': 0, '#': 1}) for schematic in schematics]
    locks, keys = [], []
    for schematic in schematics:
        if all(schematic[:,0]):
            locks.append(np.array([sum(schematic[x,:])-1 for x in range(schematic.width)]))
        else:
            keys.append(np.array([sum(schematic[x, :])-1 for x in range(schematic.width)]))
    return (locks, keys)


def solve1(locks, keys):
    fit = 0
    print(f"Matching {len(locks)} to {len(keys)}")
    for (a,b,c,d,e) in locks:
        for (f,g,h,i,j) in keys:
            #print(f"{(a,b,c,d,e)}, {(f,g,h,i,j)}")
            if max(a+f, b+g, c+h,d+i,e+j) <= 5:
                fit += 1
    return fit

def solve2(locks, keys):
    fit = 0
    print(f"Matching {len(locks)} to {len(keys)}")
    treedict = lambda depth: lambda: defaultdict(treedict(depth - 1) if depth else lambda:set())
    locktree = treedict(3)()
    keytree = treedict(3)()
    for a,b,c,d,e in locks:
        locktree[a][b][c][d].add(e)
    for a,b,c,d,e in keys:
        keytree[a][b][c][d].add(e)

    #fit = lock
    #for tumbler in range(5):
        #for lockheight, locks in locktree.items():
            #for keyheight in range(5-lockheight):
                #fit[]



def main():
    problem = read()
    print(f"Problem 1: {solve1(*problem)}")
    print(f"Problem 2: {solve2(*problem)}")


main()
