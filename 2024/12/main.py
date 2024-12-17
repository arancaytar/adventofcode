import sys
import math
import numpy as np
import heapq
from collections import Counter
from collections import deque

def read():
    return ([list(x) for x in sys.stdin.read().strip().split("\n")],)

def solve1(grid):
    width, height = len(grid[0]), len(grid)
    index = np.zeros((width, height), dtype=int) - 1
    regions = []
    region_area = {}
    region_perimeter = {}
    
    for i in range(height):
        for j in range(width):
            if index[i,j] < 0:
                c = grid[i][j]
                current = index[i,j] = len(regions)
                #print(f"New region {current} found at {(i,j)} with {grid[i][j]}.")
                regions.append(grid[i][j])
                region_area[current] = 0
                region_perimeter[current] = 0

                queue = deque([(i, j)])
                while queue:
                    i1, j1 = queue.popleft()
                    #print(f"   Expanding {current} from {(i1, j1)}.")
                    region_area[current] += 1
                    for di, dj in ((1,0), (-1, 0), (0, 1), (0, -1)):
                        i2, j2 = i1 + di, j1 + dj
                        if 0 <= i2 < height and 0 <= j2 < width:
                            c2 = grid[i2][j2]
                            if c == c2:
                                if index[i2, j2] < 0:
                                    index[i2, j2] = current
                                    #print(f"    Found neighbor {(i2, j2)}.")
                                    queue.append((i2, j2))
                            else:
                                region_perimeter[current] += 1
                        else:
                            region_perimeter[current] += 1

    print(regions, region_area, region_perimeter)
    print(index)
    for x in range(len(regions)):
        print(f"A region of {regions[x]} plants with price {region_area[x]} x {region_perimeter[x]} = {region_area[x] * region_perimeter[x]}")

    return sum(region_area[x] * region_perimeter[x] for x in range(len(regions)))
    
def solve2(grid):
    width, height = len(grid[0]), len(grid)
    index = np.zeros((width, height), dtype=int) - 1
    regions = []
    region_area = {}
    region_edges = {}
    
    for i in range(height):
        for j in range(width):
            if index[i,j] < 0:
                c = grid[i][j]
                current = index[i,j] = len(regions)
                #print(f"New region {current} found at {(i,j)} with {grid[i][j]}.")
                regions.append(grid[i][j])
                region_area[current] = 0
                region_edges[current] = {(1,0): set(), (-1, 0): set(), (0, 1): set(), (0, -1): set()}

                queue = deque([(i, j)])
                while queue:
                    i1, j1 = queue.popleft()
                    #print(f"   Expanding {current} from {(i1, j1)}.")
                    region_area[current] += 1
                    for di, dj in region_edges[current].keys():
                        i2, j2 = i1 + di, j1 + dj
                        if 0 <= i2 < height and 0 <= j2 < width:
                            c2 = grid[i2][j2]
                            if c == c2:
                                if index[i2, j2] < 0:
                                    index[i2, j2] = current
                                    #print(f"    Found neighbor {(i2, j2)}.")
                                    queue.append((i2, j2))
                            else:
                                region_edges[current][di,dj].add((i1, j1))
                        else:
                            region_edges[current][di,dj].add((i1, j1))

    region_sides = {}
    print(region_edges[0])
    for cur in range(len(regions)):
        region_sides[cur] = 0
        for (di, dj), edges in region_edges[cur].items():
            if dj:
                edges = {(j,i) for (i,j) in edges} # transpose vertical edges
            edges = sorted(edges)
            pi, pj = -2, -2
            for i, j in edges:
                if i != pi or j != pj + 1:
                    region_sides[cur] += 1
                pi, pj = i, j
#            print(edges)
            #prev = edges[0]
            #for edge in edges[1:]:
            #    if 
            #print(f"Region {cur} has {(di,dj)} edges at {edges}")
            

    #print(regions, region_area, region_edges)
    print(index)
    for x in range(len(regions)):
        print(f"A region of {regions[x]} plants with price {region_area[x]} x {region_sides[x]} = {region_area[x] * region_sides[x]}")

    return sum(region_area[x] * region_sides[x] for x in range(len(regions)))
    
def solve1(grid):
    width, height = len(grid[0]), len(grid)
    index = np.zeros((width, height), dtype=int) - 1
    regions = []
    region_area = {}
    region_perimeter = {}
    
    for i in range(height):
        for j in range(width):
            if index[i,j] < 0:
                c = grid[i][j]
                current = index[i,j] = len(regions)
                regions.append(grid[i][j])
                region_area[current] = 0
                region_perimeter[current] = 0

                queue = deque([(i, j)])
                while queue:
                    i1, j1 = queue.popleft()
                    region_area[current] += 1
                    for di, dj in ((1,0), (-1, 0), (0, 1), (0, -1)):
                        i2, j2 = i1 + di, j1 + dj
                        if 0 <= i2 < height and 0 <= j2 < width:
                            c2 = grid[i2][j2]
                            if c == c2:
                                if index[i2, j2] < 0:
                                    index[i2, j2] = current
                                    queue.append((i2, j2))
                            else:
                                region_perimeter[current] += 1
                        else:
                            region_perimeter[current] += 1

    return sum(region_area[x] * region_perimeter[x] for x in range(len(regions)))
    
def solve(grid):
    width, height = len(grid[0]), len(grid)
    index = np.zeros((width, height), dtype=int) - 1
    regions = []
    region_area = {}
    region_edges = {}
    
    for i in range(height):
        for j in range(width):
            if index[i,j] < 0:
                c = grid[i][j]
                current = index[i,j] = len(regions)
                regions.append(grid[i][j])
                region_area[current] = 0
                region_edges[current] = {(1,0): set(), (-1, 0): set(), (0, 1): set(), (0, -1): set()}

                queue = deque([(i, j)])
                while queue:
                    i1, j1 = queue.popleft()
                    region_area[current] += 1
                    for di, dj in region_edges[current].keys():
                        i2, j2 = i1 + di, j1 + dj
                        if 0 <= i2 < height and 0 <= j2 < width:
                            c2 = grid[i2][j2]
                            if c == c2:
                                if index[i2, j2] < 0:
                                    index[i2, j2] = current
                                    queue.append((i2, j2))
                                continue
                        region_edges[current][di,dj].add((i1, j1))


    region_perimeter = {x: sum(len(e) for e in edges.values()) for x, edges in region_edges.items()}
    region_sides = {}

    for cur in range(len(regions)):
        region_sides[cur] = 0
        for (di, dj), edges in region_edges[cur].items():
            if dj:
                edges = {(j,i) for (i,j) in edges} # transpose vertical edges
            edges = sorted(edges)
            pi, pj = -2, -2
            for i, j in edges:
                if i != pi or j != pj + 1:
                    region_sides[cur] += 1
                pi, pj = i, j

    print(index)
    for x in range(len(regions)):
        print(f"A region of {regions[x]} plants with price (1) {region_area[x]} x {region_sides[x]} = {region_area[x] * region_sides[x]}, (2) {region_area[x]} x {region_perimeter[x]} = {region_area[x] * region_perimeter[x]}")

    return (
        sum(region_area[x] * region_perimeter[x] for x in range(len(regions)))
        sum(region_area[x] * region_sides[x] for x in range(len(regions))),
    )
    

    
def main():
    problem = read()
    print(f"Problem 1: {solve1(*problem)}")
    print(f"Problem 2: {solve2(*problem)}")
    print(f"Problem 1+2: {solve(*problem)}")

def debug():
    return None
    

main()
#debug()