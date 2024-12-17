import sys
import numpy as np
import collections
import typing
def step_snowstorms(snowstorms: typing.Dict[typing.Tuple[int, int], int]) -> typing.Dict[typing.Tuple[int, int], int]:
    snowstorms_next = collections.defaultdict(set)
    for (x, y), directions in snowstorms.items():
        for dx, dy in directions:
            snowstorms_next[(x+dx)%w,(y+dy)%h].add((dx, dy))
    return snowstorms_next

def step_me(locations: typing.Set[typing.Tuple[int, int]], snowstorms_next: typing.Dict[typing.Tuple[int, int], int]) -> typing.Set[typing.Tuple[int, int]]:
    locations_next = set.union(*(
        {
            (x+dx, y+dy) for dx, dy in
            ((0, 0), (1, 0), (-1, 0), (0, 1), (0, -1))
            if valid(x+dx, y+dy)
        }
        for x,y in locations
    ))
    locations_next -= snowstorms_next.keys()
    return locations_next

def valid(x: int, y: int) -> bool:
    return (0 <= x < w and 0 <= y < h) or (x, y) ==  destination or (x, y) == start

def solve1(start, destination, snowstorms):
    locations = {start}
    counter = 0
    while destination not in locations:
        snowstorms = step_snowstorms(snowstorms)
        locations = step_me(locations, snowstorms)
        counter += 1
    return counter

def solve2(start, destination, snowstorms):
    locations = {start}
    counter = 0
    while destination not in locations:
        snowstorms = step_snowstorms(snowstorms)
        locations = step_me(locations, snowstorms)
        counter += 1
    locations = {destination}
    while start not in locations:
        snowstorms = step_snowstorms(snowstorms)
        locations = step_me(locations, snowstorms)
        counter += 1
    locations = {start}
    while destination not in locations:
        snowstorms = step_snowstorms(snowstorms)
        locations = step_me(locations, snowstorms)
        counter += 1
    return counter


def read(data):
    key = {'.': 0, '#': 1, '^': 2, '>': 3, 'v': 4, '<': 5}
    directions = {2: (0, -1), 3: (1, 0), 4: (0, 1), 5: (-1, 0)}
    matrix = np.array([[key[x] for x in line] for line in data.split("\n")])
    h, w = matrix.shape
    start = (list(matrix[0,:]).index(0) - 1, - 1)
    destination = (list(matrix[h - 1, :]).index(0) - 1, h - 2)
    snowstorms = {(x-1, y-1): {directions[matrix[y, x]]} for y in range(1, h) for x in range(1, w) if matrix[y, x] > 1}
    return start, destination, snowstorms, (h-2, w-2)


start, destination, snowstorms, (h, w) = read(sys.stdin.read())
print(solve1(start, destination, snowstorms))
print(solve2(start, destination, snowstorms))
