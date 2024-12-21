from grid import Grid
from graph import dijkstra,DGraph
import sys
import numpy as np
from collections import Counter, deque
def read():
    grid = Grid.read(sys.stdin.read())
    start = end = None
    for (x, y), c in grid:
        if c == 'S':
            start = x, y
        elif c == 'E':
            end = x, y
    return grid, start, end


def solve1(grid, start, end):
    class _Graph(DGraph):
        def outgoing(self, u):
            x, y = u
            for (x2, y2), c in grid.neighbors4(x, y):
                if c != '#':
                    yield (x2, y2), 1


    distance_end, predecessor = dijkstra(_Graph(), end, -np.ones((grid.width, grid.height), dtype=int))

    shortcuts = {}
    for (x, y), c in grid:
        if c == '#':
            shortcut_starts = {}
            shortcut_ends = {}
            for (x2, y2), c2 in grid.neighbors4(x, y):
                if c2 != '#':
                    shortcut_starts[x2,y2] = distance_end[x2,y2]
                    shortcut_ends[x2,y2] = distance_end[x2,y2]
            for start, cost1 in shortcut_starts.items():
                for end, cost2 in shortcut_ends.items():
                    if cost1 > cost2 + 2:
                        shortcuts[start,end] = cost1 - cost2 - 2
    return sum(x >= 100 for x in shortcuts.values())

def solve2(grid, start, end):
    class _Graph(DGraph):
        def outgoing(self, u):
            x, y = u
            for (x2, y2), c in grid.neighbors4(x, y):
                if c != '#':
                    yield (x2, y2), 1

    distance_end, predecessor = dijkstra(_Graph(), end, -np.ones((grid.width, grid.height), dtype=int))

    shortcuts = {}
    for (x, y), c in grid:
        if c != '#':
            cost1 = distance_end[x, y]
            for (x2, y2), c2 in grid.neighbors_distance(x, y, 20):
                if c2 != '#':
                    #print(f"Checking {x,y} to {x2,y2} with distance {abs(x-x2) + abs(y - y2)}.")
                    cost2 = distance_end[x2,y2] + abs(x - x2) + abs(y - y2)
                    if cost1 > cost2:
                        shortcuts[(x,y),(x2,y2)] = cost1 - cost2
            #break
    db = Counter(shortcuts.values())
    #for x in sorted(db.keys()):
    #    if x >= 50:
    #        print(f"There are {db[x]} cheats that save {x} picoseconds.")
    return sum(x >= 100 for x in shortcuts.values())

def solve2(grid, start, end):
    class _Graph(DGraph):
        def outgoing(self, u):
            x, y = u
            for (x2, y2), c in grid.neighbors4(x, y):
                if c != '#':
                    yield (x2, y2), 1

    distance_end, predecessor = dijkstra(_Graph(), end, -np.ones((grid.width, grid.height), dtype=int))

    shortcuts = 0
    for (x, y), c in grid:
        if c != '#':
            cost1 = distance_end[x, y]
            candidates = deque()
            for (x2, y2), c2 in grid.neighbors_distance_exact(x, y, 20):
                #print(x,y,x2,y2)
                if c2 != '#':
                    cost2 = distance_end[x2,y2]
                    if cost1 >= cost2 + 120:
                        candidates.append((x2, y2, 120))
            print(x,y, len(candidates))
            while candidates:
                x2, y2, d = candidates.popleft()
                shortcuts += 1
                if x2 < x and distance_end[x2+1,y2] + d - 1 <= cost1:
                    candidates.append((x2 + 1, y2, d - 1))
                elif x2 > x and distance_end[x2-1,y2] + d - 1 <= cost1:
                    candidates.append((x2 - 1, y2, d - 1))
                if y2 < y and distance_end[x2,y2+1] + d - 1 <= cost1:
                    candidates.append((x2, y2 + 1, d - 1))
                elif y2 > y and distance_end[x2-1,y2] + d - 1 <= cost1:
                    candidates.append((x2, y2 - 1, d - 1))

    return shortcuts

def main():
    problem = read()
    print(f"Problem 1: {solve1(*problem)}")
    print(f"Problem 2: {solve2(*problem)}")

main()