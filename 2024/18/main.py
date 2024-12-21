import sys
import re
import numpy as np
from collections import deque
from grid import Grid
from graph import DGraph, bfs

def read():
    return ([tuple(map(int, row.split(","))) for row in sys.stdin.read().strip().split("\n")],)

def solve1(coords):
    w, h, steps = 71, 71, 1024
    
    #w, h, steps = 7, 7, 12
    data = np.zeros((w, h), dtype=bool)
    for x,y in coords[:steps]:
        data[x, y] = 1
        
    grid = Grid(data)
    class _Graph(DGraph):
        def outgoing(self, u):
            x, y = u
            for (x2, y2), c in grid.neighbors4(x, y):
                if not c:
                    yield x2, y2

    cost, predecessor = bfs(_Graph(), (0,0), (w-1, h-1), -np.ones((grid.width, grid.height), dtype=int))
    return cost

def backtrace(grid, predecessors, states):
    visited = np.zeros((grid.width, grid.height), dtype=bool)
    while states:
        pre = set()
        for x,y in states:
            pre |= predecessors[x,y] or set()
            visited[x,y] = True
        states = pre
    return visited

def solve2(coords):
    w, h = 71, 71 
    #w, h = 7, 7
    data = -np.ones((w, h))
    for i,(x,y) in enumerate(coords):
        data[x, y] = i
    grid = Grid(data)
    

    class _Graph(DGraph):
        def __init__(self, time):
            self.time = time
        def outgoing(self, u):
            x, y = u
            for (x2, y2), c in grid.neighbors4(x, y):
                if not 0 <= c < self.time:
                    yield (x2, y2)
    
    a, b = 0, len(coords)
    
    # We know the empty grid is not obstructed at the start.
    # Check if it is ever obstructed, to ensure there's a valid answer:
    dist, predecessor = bfs(_Graph(b), (0,0), (w-1, h-1), -np.ones((grid.width, grid.height), dtype=int))
    if dist >= 0:
        return f"The grid is never obstructed."

    while a + 1 < b:
        c = (a + b) // 2
        dist, predecessor = bfs(_Graph(c), (0,0), (w-1, h-1), -np.ones((grid.width, grid.height), dtype=int))
        if dist < 0:
            b = c # grid is obstructed
        else:
            a = c # grid is navigable
        print(a,b)
    x, y = coords[a]
    return f"#{a}: {x},{y}"


def solve3(coords):
    w, h = 71, 71 
    #w, h = 7, 7
    data = -np.ones((w, h))
    for i,(x,y) in enumerate(coords):
        data[x, y] = i
    grid = Grid(data)
    

    class _Graph(DGraph):
        def __init__(self, time):
            self.time = time
        def outgoing(self, u, t):
            x, y = u
            for (x2, y2), c in grid.neighbors4(x, y):
                if not 0 <= c < self.time + t:
                    yield (x2, y2)
    
    a, b = -len(coords), len(coords)

    dist, predecessor = bfs_modified(_Graph(b), (0,0), (w-1, h-1), -np.ones((grid.width, grid.height), dtype=int))
    if dist >= 0:
        return f"The grid is never obstructed."

    while a + 1 < b:
        c = (a + b) // 2
        dist, predecessor = bfs_modified(_Graph(c), (0,0), (w-1, h-1), -np.ones((grid.width, grid.height), dtype=int))
        if dist < 0:
            b = c # grid is obstructed
        else:
            a = c # grid is navigable
        print(a,b)
    x, y = coords[a]
    return f"#{a}: {x},{y}"

def bfs_modified(graph, start, end=None, distance=None, predecessor=None):
    Q = deque([(0, start)])
    while Q:
        d, u = Q.popleft()
        if distance[u] >= 0:
            continue
        distance[u] = d
        for v in graph.outgoing(u, d):
            if distance[v] < 0:
                if v == end:
                    return d + 1, predecessor
                Q.append((d + 1, v))
    if end is None:
        return distance, predecessor
    else:
        return -1, None

def main():
    problem = read()
    print(f"Problem 1: {solve1(*problem)}")
    print(f"Problem 2: {solve2(*problem)}")
    print(f"Problem 3: {solve3(*problem)}")
    

    
    
main()