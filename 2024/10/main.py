import sys
import math
import numpy as np
import heapq
from collections import Counter

def read():
    return (np.array([list(map(int, line)) for line in sys.stdin.read().strip().split("\n")]),)

def solve1(grid):
    width, height = grid.shape
    trail_heads = {}
    for i in range(height):
        for j in range(width):
            if grid[i,j] == 0:
                reachable = {(i,j)}
                for dist in range(1,10):
                    reachable2 = set()
                    for i1, j1 in reachable:
                        for di, dj in [(1,0), (-1, 0), (0, 1), (0, -1)]:
                            i2, j2 = i1 + di, j1 + dj
                            if 0 <= i2 < height and 0 <= j2 < width and grid[i2,j2] == dist:
                                reachable2.add((i2, j2))
                    reachable = reachable2
                trail_heads[(i, j)] = len(reachable)
    return sum(trail_heads.values())

def solve2(grid):
    width, height = grid.shape
    trail_heads = {}
    for i in range(height):
        for j in range(width):
            if grid[i,j] == 0:
                reachable = Counter([(i,j)])
                for dist in range(1,10):
                    reachable2 = Counter()
                    for (i1, j1), distinct in reachable.items():
                        for di, dj in [(1,0), (-1, 0), (0, 1), (0, -1)]:
                            i2, j2 = i1 + di, j1 + dj
                            if 0 <= i2 < height and 0 <= j2 < width and grid[i2,j2] == dist:
                                reachable2[(i2, j2)] += distinct
                    reachable = reachable2
                trail_heads[(i, j)] = sum(reachable.values())
    return sum(trail_heads.values())

def solve2_fast(grid):
    width, height = grid.shape
    reachable = Counter((i,j) for i in range(height) for j in range(width) if grid[i,j] == 0)
    for dist in range(1,10):
        reachable2 = Counter()
        for (i1, j1), distinct in reachable.items():
            for di, dj in [(1,0), (-1, 0), (0, 1), (0, -1)]:
                i2, j2 = i1 + di, j1 + dj
                if 0 <= i2 < height and 0 <= j2 < width and grid[i2,j2] == dist:
                    reachable2[(i2, j2)] += distinct
        reachable = reachable2
    return sum(reachable.values())

def solve(grid, part=1):
    width, height = grid.shape
    trail_heads = {}
    for i in range(height):
        for j in range(width):
            if grid[i,j] == 0:
                reachable = Counter([(i,j)])
                for dist in range(1,10):
                    reachable2 = Counter()
                    for (i1, j1), distinct in reachable.items():
                        for di, dj in [(1,0), (-1, 0), (0, 1), (0, -1)]:
                            i2, j2 = i1 + di, j1 + dj
                            if 0 <= i2 < height and 0 <= j2 < width and grid[i2,j2] == dist:
                                reachable2[(i2, j2)] += distinct
                    reachable = reachable2
                trail_heads[(i, j)] = sum(reachable.values()) if part == 2 else len(reachable)
    return sum(trail_heads.values())
    
def main():
    problem = read()
    #print(f"Problem 1: {solve1(*problem)}")
    #print(f"Problem 2: {solve2(*problem)}")
    print(f"Problem 2: {solve2_fast(*problem)}")
    #print(f"Problem 1,2: {solve(*problem, part=1), solve(*problem, part=2)}")

def debug():
    return None
    

main()
#debug()