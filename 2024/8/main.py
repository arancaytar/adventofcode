import sys
import math

def read():
    grid = sys.stdin.read().strip().split("\n")
    frequencies = {x: set() for row in grid for x in row if x != '.'}
    for i, row in enumerate(grid):
        for j, freq in enumerate(row):
            if freq != '.':
                frequencies[freq].add((i,j))
    bounds = len(grid[0]), len(grid)
    return bounds, frequencies


def solve1(bounds, frequencies):
    antinodes = set()
    width, height = bounds
    for frequency, antennae in frequencies.items():
        for i, (x1, y1) in enumerate(antennae):
            for j, (x2, y2) in enumerate(antennae):
                if i != j:
                    ax, ay = 2*x2 - x1, 2*y2 - y1
                    if 0 <= ax < width and 0 <= ay < height:
                        antinodes.add((ax, ay))
    return len(antinodes)

   
def solve2(bounds, frequencies):
    antinodes = set()
    width, height = bounds
    for frequency, antennae in frequencies.items():
        for i, (x1, y1) in enumerate(antennae):
            for j, (x2, y2) in enumerate(antennae):
                if i != j:
                    dx, dy = x2 - x1, y2 - y1
                    target_x = -1 if dx < 0 else width
                    target_y = -1 if dy < 0 else height
                    antinodes |= set(zip(range(x1 + dx, target_x, dx), range(y1 + dy, target_y, dy)))
    return len(antinodes)
     
def display(grid, visited, x, y, h):
    icon = {1: '^', 2: '>', 4: 'v', 8: '<'}[h]
    height, width = grid.shape
    output = [['.#x'[grid[i,j] + 2*(visited[i,j] > 0)] for j in range(width)] for i in range(height)]
    output[y][x] = icon
    print("\n".join("".join(row) for row in output))
   
def main():
    problem = read()
    print(f"Problem 1: {solve1(*problem)}")
    print(f"Problem 2: {solve2(*problem)}")

def debug():
    return None
    

main()
#debug()