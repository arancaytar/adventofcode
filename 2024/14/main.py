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

def read():
    robots = sys.stdin.read().strip().split("\n")
    print(robots)
    return [list(map(int, re.match(r"p=(\d+),(\d+) v=(-?\d+),(-?\d+)", robot).groups())) for robot in robots]

def solve1(*robots):
    time = 100
    #width, height = 11, 7 (sample)
    width, height = 101, 103
    robots = [(px, py, vx + width, vy + height) for (px, py, vx, vy) in robots]
    final = [((px + time * vx) % width, (py + time * vy) % height) for px, py, vx, vy in robots]
    
    quadrants = [0] * 4
    for x, y in final:
        if x != width // 2 and y != height // 2:
            quadrants[2*(y > height // 2) + (x > width // 2)] += 1
    return reduce(mul, quadrants, 1)
    
def solve2(*robots):
    width, height = 101, 103
    robots = [(px, py, vx + width, vy + height) for (px, py, vx, vy) in robots]
    positions = [(px, py) for (px, py, vx, vy) in robots]
    velocities = [(vx, vy) for (px, py, vx, vy) in robots]
    scores = [0]
    for i in range(1, 10000):
        positions = [((px + vx) % width, (py + vy) % height) for ((px, py), (vx, vy)) in zip(positions, velocities)]
        grid = aggregate(positions, width, height)
        score = 0
        for x, y in positions:
            for dx, dy in ((-1, 0), (1, 0), (0, 1), (0, -1)):
                x2, y2 = x + dx, y + dy
                if 0 <= x2 < width and 0 <= y2 < height and grid[y2][x2] == '#':
                    score += 1
        scores.append(score)
        if score > 500:
            print(i)
            display(grid)
    best = max(range(len(scores)), key = lambda x:scores[x])
    return best

def aggregate(robots, width, height):
    grid = [['.']*width for i in range(height)]
    for x, y in robots:
        grid[y][x] = '#'
    return grid
    
def display(grid):
    print("\n".join("".join(line) for line in grid))
    
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



 