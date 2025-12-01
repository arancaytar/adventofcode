import sys
import math
import numpy as np
import sympy as sp
import heapq
from collections import Counter
from collections import deque
import re
from fractions import Fraction
from functools import reduce
from operator import mul
from grid import Grid

def read():
    grid, instructions = sys.stdin.read().strip().split("\n\n")
    grid = Grid.read(grid)
    instructions = list(instructions.replace("\n", ""))
    for (x, y), c in grid:
        if c == '@':
            grid[x,y] = '.'
            return grid, instructions, (j, i)
    raise ValueError("No starting position")

def solve1(grid, instructions, start):
    grid = copy(grid)
    x, y = start
    width, height = grid.width, grid.height
    lookup = {"^": (0, -1), ">": (1, 0), "v": (0, 1), "<": (-1, 0)}
    boxes = set()
    for (x,y), c in grid:
        if c == 'O':
            boxes.add((x,y))
    for move in instructions:
        dx, dy = lookup[move]
        x2, y2 = x + dx, y + dy
        x3, y3 = x2, y2
        while grid[x3,y3] == 'O':
            x3, y3 = x3 + dx, y3 + dy
        if grid[x3,y3] == '#':
            continue # hit a wall
        else:
            grid[x3,y3] = 'O' # move all boxes one step
            grid[x2,y2] = '.'
            boxes.add((x3, y3))
            boxes.remove((x2, y2))
            x, y = x2, y2
    return sum(x + 100*y for x, y in boxes)
            
def solve2(grid, instructions, start):
    display_grid(grid)
    grid, start = widen(grid, start)
    display_grid(grid)
    width, height = grid.width, grid.height
    lookup = {"^": (0, -1), ">": (1, 0), "v": (0, 1), "<": (-1, 0)}
    boxes = set()    
    for (x,y), c in grid:
        if c == '[':
            boxes.add((x, y))
    x, y = start
    for move in instructions:
        def try_move(x2, y2):
            targets = set()
            check = {(x2, y2)}
            free = set()
            while not check <= free:
                check2 = set()
                free2 = set()
                for x3, y3 in check:
                    if grid[x3,y3] == '#':
                        return False, set()
                    elif {(x3, y3), (x3 - 1, y3)} & targets:
                        continue # if we already know we're moving a box from here, no need to check it again
                    elif (x3, y3) in boxes: # hit a box's left side
                        targets.add((x3, y3))
                        check2 |= {(x3 + dx, y3 + dy), (x3 + 1 + dx, y3 + dy)}
                    elif (x3 - 1, y3) in boxes: # hit a box's right side
                        targets.add((x3 - 1, y3))
                        check2 |= {(x3 - 1 + dx, y3 + dy), (x3 + dx, y3 + dy)}
                    elif grid[x3,y3] == '.':
                        free2.add((x3, y3))
                check, free = check2, free2
            return True, targets
            
        dx, dy = lookup[move]
        x2, y2 = x + dx, y + dy
        success, targets = try_move(x2, y2)
        if success:
            boxes = boxes - targets | {(x + dx, y + dy) for x, y in targets}
            for x, y in targets:
                grid[x:x+2,y] = ['.', '.']
            for x, y in targets:
                grid[x+dx:x+dx+2,y] = ['[', ']']
            x, y = x2, y2
    display_grid(grid)
        
    return sum(x + 100*y for x, y in boxes)

def widen(grid, start):
    x, y = start
    width, height = len(grid[0]), len(grid)
    grid2 = [[None] * width*2 for i in range(height)]
    for i in range(height):
        for j in range(width):
            if grid[i][j] == 'O':
                grid2[i][2*j:2*j+2] = ['[', ']']
            else:
                grid2[i][2*j:2*j+2] = [grid[i][j]] * 2
    return grid2, (x*2, y)

def display_grid(grid):
    print("\n".join("".join(row) for row in grid))



def main():
    problem = read()
    #print(f"S: {sample2()}")
    print(f"Problem 1: {solve1(*problem)}")
    print(f"Problem 2: {solve2(*problem)}")
    #print(f"Problem 1+2: {solve(*problem)}")

def debug():
    return None
    

main()
#debug()



 