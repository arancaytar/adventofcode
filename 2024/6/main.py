import sys
from functools import cmp_to_key
import numpy as np

def read():
    data = sys.stdin.read().strip().split("\n")
    w, h = len(data), len(data[0])
    grid = np.zeros((h,w), dtype=int)
    guard = None
    for i, row in enumerate(data):
        for j, c in enumerate(row):
            if c == '#':
                grid[i,j] = 1
            elif c == '^':
                guard = i, j, 1
    return grid, guard

def guard_step(x, y, h):
    return x + (h == 2) - (h == 8), y - (h == 1) + (h == 4)

def solve1(grid, guard):
    visited = np.zeros(grid.shape, dtype=int)
    height, width = grid.shape
    y, x, h = guard
    while not visited[y, x] & h:
        #display(grid, visited, x, y, h)
        visited[y, x] |= h
        next_x, next_y = guard_step(x, y, h)
        #print(f"Guard at {x,y} heading {h}, trying to move to {next_x, next_y}")
        if not (0 <= next_x < width and 0 <= next_y < height):
            #print("Leaving the area")
            break
        if grid[next_y, next_x]:
            h = h<<1 & 15 or 1
            #print(f"Obstacle, turning to {h}")
        else:
            x, y = next_x, next_y
    return (visited > 0).sum()

def check_loop(grid, guard, visited = None):
    visited = visited.copy() if (visited is not None) else np.zeros(grid.shape, dtype=int)
    height, width = grid.shape
    y, x, h = guard
    #print("Checking for loop...")
    while not visited[y, x] & h:
        #display(grid, visited, x, y, h)
        visited[y, x] |= h
        next_x, next_y = guard_step(x, y, h)
        #print(f"    Guard at {x,y} heading {h}, trying to move to {next_x, next_y}")
        if not (0 <= next_x < width and 0 <= next_y < height):
            #print("    Leaving the area")
            #print("No loop found.")
            return False
        if grid[next_y, next_x]:
            h = h<<1 & 15 or 1
            #print(f"    Obstacle, turning to {h}")
        else:
            x, y = next_x, next_y
    #print("Loop found.")
    return True

def add_obstacle(grid, i, j):
    grid2 = grid.copy()
    grid2[i,j] = 1
    return grid2
    
def solve2(grid, guard):
    visited = np.zeros(grid.shape, dtype=int)
    height, width = grid.shape
    y, x, h = guard
    loop_options = 0
    while not visited[y, x] & h:
        #display(grid, visited, x, y, h)
        visited[y, x] |= h
        next_x, next_y = guard_step(x, y, h)
        #print(f"Guard at {x,y} heading {h}, trying to move to {next_x, next_y}")
        if not (0 <= next_x < width and 0 <= next_y < height):
            #print("Leaving the area")
            break
        if grid[next_y, next_x]:
            h = h<<1 & 15 or 1
            #print(f"Obstacle, turning to {h}")
        else:
            x, y = next_x, next_y
    for i in range(height):
        for j in range(width):
            if (i, j, 1) != guard and visited[i,j]:
                loop_options += check_loop(add_obstacle(grid, i, j), guard)
    return loop_options

def solve2_faster(grid, guard):
    visited = np.zeros(grid.shape, dtype=int)
    height, width = grid.shape
    y, x, h = guard
    loop_options = 0
    while not visited[y, x] & h:
        #display(grid, visited, x, y, h)
        next_x, next_y = guard_step(x, y, h)
        #print(f"Guard at {x,y} heading {h}, trying to move to {next_x, next_y}")
        if not (0 <= next_x < width and 0 <= next_y < height):
            #print("Leaving the area")
            break
        if grid[next_y, next_x]:
            visited[y, x] |= h
            h = h<<1 & 15 or 1
            #print(f"Obstacle, turning to {h}")
        else:
            if not visited[next_y,next_x]: # only block squares we haven't already visited
                #print(f"Trying to add obstacle at {next_x, next_y}")
                loop_options += check_loop(add_obstacle(grid, next_y, next_x), (y, x, h), visited)
                #print(f"Total loop options: {loop_options}")
            visited[y, x] |= h
            x, y = next_x, next_y
        
    return loop_options
        
def display(grid, visited, x, y, h):
    icon = {1: '^', 2: '>', 4: 'v', 8: '<'}[h]
    height, width = grid.shape
    output = [['.#x'[grid[i,j] + 2*(visited[i,j] > 0)] for j in range(width)] for i in range(height)]
    output[y][x] = icon
    print("\n".join("".join(row) for row in output))
   
def main():
    problem = read()
    print(f"Problem 1: {solve1(*problem)}")
    print(f"Problem 2: {solve2_faster(*problem)}")

def debug():
    return None
    

main()
#debug()