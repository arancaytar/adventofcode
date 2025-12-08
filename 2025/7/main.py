import sys
import grid
import numpy as np

def read():
    return grid.Grid.read(sys.stdin.read(), {'.': 0, 'S':1, '^':1})

def solve1(g):
    run = g[:,0]
    splits = 0
    for y in range(1, g.height):
        splits += sum(run & g[:,y])
        run = (run > g[:,y]) | np.roll(run & g[:,y], -1) | np.roll(run & g[:,y], 1)
    return splits

def solve2(g):
    run = g[:,0].astype(np.uint64)
    for y in range(1, g.height):
        run = ((run * (1-g[:,y])) + np.roll(run * g[:,y], -1) + np.roll(run * g[:,y], 1)).astype(np.uint64)
    return run.sum()

def main():
    g = read()
    print(solve1(g))
    print(solve2(g))

main()
