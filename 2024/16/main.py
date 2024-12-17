import sys
import math
import numpy as np
#import sympy as sp
#import heapq
#from collections import Counter
#from collections import deque
#import re
#from fractions import Fraction
#from functools import reduce
#from operator import mul
from graph import bellman_ford_moore, DGraph, dijkstra
from grid import Grid

def read():
    grid = [list(row) for row in sys.stdin.read().strip().split("\n")]
    start = end = None
    for i, row in enumerate(grid):
        for j, c in enumerate(row):
            if c == 'S':
                start = j, i
            elif c == 'E':
                end = j, i
            grid[i][j] = c == '#'
    return np.array(grid, dtype=bool), start, end

def solve1(grid, start, end):
    max_int = 2**64
    width, height = grid.shape
    solutions = np.zeros((width, height, 4), dtype=int) + max_int
    x_start, y_start = start
    x_end, y_end = end
    positions = {(x_start, y_start, 0)}
    solutions[x_start, y_start, 0] = 0
    headings = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    while positions:
        #print(positions)
        new_positions = set()
        for x, y, h in positions:
            current = int(solutions[x, y, h])
            #print(f"Starting from {x,y} facing {h} cost {current}.")
            move = 1 + current
            turn = 1000 + current
            dx, dy = headings[h]
            x2, y2 = x + dx, y + dy
            if not grid[y2, x2] and solutions[x2, y2, h] > move:
                #print(f"Can move to {x2,y2} for {move}.")
                solutions[x2, y2, h] = move
                new_positions.add((x2, y2, h))
            nh, ph = (h + 1) % 4, (h + 3) % 4
            if solutions[x, y, nh] > turn:
                #print(f"Can turn right to {nh} for {turn}.")
                solutions[x, y, nh] = turn
                new_positions.add((x, y, nh))
            if solutions[x, y, ph] > turn:
                #print(f"Can turn left to {ph} for {turn}.")
                solutions[x, y, ph] = turn
                new_positions.add((x, y, ph))
        positions = new_positions
        #print(positions)
        #print(solutions)
        #print("-----")

    #grid2 = backtrace(grid, solutions, end)
    
    return min(solutions[x_end, y_end,:])


            
def solve(grid, start):
    max_int = 2**64
    width, height = grid.shape
    solutions = np.zeros((width, height, 4), dtype=int) + max_int
    x_start, y_start = start
    positions = {(x_start, y_start, 0)}
    solutions[x_start, y_start, 0] = 0
    headings = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    while positions:
        new_positions = set()
        for x, y, h in positions:
            current = int(solutions[x, y, h])
            move = 1 + current
            turn = 1000 + current
            dx, dy = headings[h]
            x2, y2 = x + dx, y + dy
            if not grid[y2, x2] and solutions[x2, y2, h] > move:
                solutions[x2, y2, h] = move
                new_positions.add((x2, y2, h))
            nh, ph = (h + 1) % 4, (h + 3) % 4
            if solutions[x, y, nh] > turn:
                solutions[x, y, nh] = turn
                new_positions.add((x, y, nh))
            if solutions[x, y, ph] > turn:
                solutions[x, y, ph] = turn
                new_positions.add((x, y, ph))
        positions = new_positions
    return solutions

def backtrace(grid, solutions, end):
    headings = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    x, y = end
    cost = min(solutions[x, y,:])
    
    positions = set()
    for h in range(4):
        if solutions[x,y,h] == cost:
            positions.add((x, y, h))
    
    
    best = np.zeros(grid.shape, dtype=int)
    best[y,x] = True
    while positions:
        new_positions = set()
        for x, y, h in positions:
            cost = solutions[x, y, h]
            dx, dy = headings[h]
            x2, y2 = x - dx, y - dy
            move = cost - 1
            turn = cost - 1000
            if solutions[x2, y2, h] == move:
                new_positions.add((x2, y2, h))
                best[y2,x2] = True
            nh, ph = (h + 3) % 4, (h + 1) % 4
            if solutions[x, y, nh] == turn:
                new_positions.add((x, y, nh))
            if solutions[x, y, ph] == turn:
                new_positions.add((x, y, ph))
        positions = new_positions
    return best


def solve1(grid, start, end):
    x, y = end
    return min(solve(grid, start)[x, y, :])

def solve2(grid, start, end):
    return backtrace(grid, solve(grid, start), end).sum()

def solve_bf(grid, start, end):
    headings = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    class _Graph(DGraph):
        def outgoing(self, u):
            x, y, h = u
            dx, dy = headings[h]
            x2, y2 = x + dx, y + dy
            if grid[x2, y2] != '#':
                yield (x2, y2, h), 1
            yield (x, y, (h + 1) % 4), 1000
            yield (x, y, (h + 3) % 4), 1000
    
    return bellman_ford_moore(_Graph(), start + (0,), np.ones((grid.width, grid.height, 4), dtype=int) * 2**64)
#    x, y = end
#    return min(cost[x,y,:])

def solve_dijkstra(grid, start):
    headings = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    class _Graph(DGraph):
        def outgoing(self, u):
            x, y, h = u
            dx, dy = headings[h]
            x2, y2 = x + dx, y + dy
            if grid[x2, y2] != '#':
                yield (x2, y2, h), 1
            yield (x, y, (h + 1) % 4), 1000
            yield (x, y, (h + 3) % 4), 1000
    
    return dijkstra(_Graph(), start + (0,), np.ones((grid.width, grid.height, 4), dtype=int) * 2**64)
#    x, y = end
#    return cost, predecessormin(cost[x,y,:])

def read():
    grid = Grid(sys.stdin.read())
    start = end = None
    for (x, y), c in grid:
        if c == 'S':
            start = x, y
        elif c == 'E':
            end = x, y
    return grid, start, end


def solve1(grid, start, end):
    cost, predecessor = solve_dijkstra(grid, start)
    return min(cost[end[0],end[1],:])

def backtrace(grid, predecessors, states):
    visited = np.zeros((grid.width, grid.height), dtype=bool)
    while states:
        pre = set()
        for x,y,h in states:
            pre |= predecessors[x,y,h] or set()
            visited[x,y] = True
        states = pre
    return visited

def solve2(grid, start, end):
    cost, predecessors = solve_dijkstra(grid, start)
    x, y = end
    c = min(cost[x,y,:])
    headings = filter(lambda h: cost[x,y,h] == c, range(4))
    return backtrace(grid, predecessors, {(x,y,h) for h in headings}).sum()
    

def main():
    problem = read()
    #print(f"S: {sample2()}")
    print(f"Problem 1: {solve1(*problem)}")
    #print(f"Problem 1: {solve_bf(*problem)}")
    #print(f"Problem 1: {solve_dijkstra(*problem)}")
    print(f"Problem 2: {solve2(*problem)}")
    #print(f"Problem 1+2: {solve(*problem)}")

def debug():
    return None
    

main()
#debug()



 