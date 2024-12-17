import sys
import typing
import numpy as np
import collections
def main(data):
    def step_snowstorms(snowstorms: typing.Dict[typing.Tuple[int, int], int]) -> typing.Dict[typing.Tuple[int, int], int]:
        snowstorms_next = collections.defaultdict(set)
        for (x, y), directions in snowstorms.items():
            for dx, dy in directions:
                snowstorms_next[(x+dx)%w,(y+dy)%h].add((dx, dy))
        return snowstorms_next

    def step_me(locations: typing.Set[typing.Tuple[int, int]], snowstorms_next: typing.Dict[typing.Tuple[int, int], int]) -> typing.Set[typing.Tuple[int, int]]:
        locations_next = set.union(*({(x+dx, y+dy) for dx, dy in ((0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)) if valid(x+dx, y+dy)} for x,y in locations))
        locations_next -= snowstorms_next.keys()
        return locations_next

    def step_me2(locations: typing.Dict[typing.Tuple[int, int], typing.Set[int]], snowstorms_next: typing.Dict[typing.Tuple[int, int], int], goals: typing.List[typing.Tuple[int, int]]) -> typing.Set[typing.Tuple[int, int]]:
        locations_next = collections.defaultdict(set)
        for (x, y),states in locations.items():
            for dx, dy in ((0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)):
                x2, y2 = x+dx, y+dy
                if valid(x2, y2) and (x2, y2) not in snowstorms_next:
                    locations_next[x2,y2] |= {state+(state < len(goals) and (x2, y2) == goals[state]) for state in states}
        return locations_next

    def valid(x: int, y: int) -> bool:
        return (0 <= x < w and 0 <= y < h) or (x, y) ==  destination or (x, y) == start
    def solve1(start, destination, snowstorms):
        locations = {start}
        counter = 0
        while destination not in locations:
            print(counter)
            draw(locations, snowstorms)
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

    def draw(locations, snowstorms):
        matrix = np.zeros((h+2, w+2), dtype=int)
        matrix[:, 0] = 1
        matrix[:, w+1] = 1
        matrix[0, :] = 1
        matrix[h+1, :] = 1
        for (x,y), direction in snowstorms.items():
            matrix[y+1,x+1] = 7 if len(direction) > 1 else {(0, -1): 2, (1, 0): 3, (0, 1): 4, (-1, 0): 5}[list(direction)[0]]

        for x,y in locations:
            matrix[y+1,x+1] = 6
        key = '.#^>v<E*'
        print("\n".join(''.join(key[matrix[y,x]] for x in range(w+2)) for y in range(h+2)))

    def read(data):
        key = {'.': 0, '#': 1, '^': 2, '>': 3, 'v': 4, '<': 5}
        directions = {2: (0, -1), 3: (1, 0), 4: (0, 1), 5: (-1, 0)}
        matrix = np.array([[key[x] for x in line] for line in data.split("\n")])
        h, w = matrix.shape
        start = (list(matrix[0,:]).index(0) - 1, - 1)
        destination = (list(matrix[h - 1, :]).index(0) - 1, h - 2)
        snowstorms = {(x-1, y-1): {directions[matrix[y, x]]} for y in range(1, h) for x in range(1, w) if matrix[y, x] > 1}
        return start, destination, snowstorms, (h-2, w-2)

    start, destination, snowstorms, (h, w) = read(data)
    #print(solve1(start, destination, snowstorms))
    print(solve2(start, destination, snowstorms))

data = sys.stdin.read().strip()
main(data)
