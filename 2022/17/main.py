import sys
import numpy as np

class Grid:
    def __init__(self, a=None, height=0):
        self.a = list(a or [])
        self.height = max(height, len(self.a))
        self.cut = self.height - len(self.a)
        self.heights = [-1]*7
        for y, row in enumerate(self.a):
            for x, cell in enumerate(row):
                if cell:
                    self.heights[x] = y + self.cut
        self.recut()

    def recut(self):
        r = min(self.heights) # all columns have at least one block up to this height.
        if r >= self.cut:
            self.a = self.a[r + 1 - self.cut:]
            self.cut = r + 1

    def __getitem__(self, position):
        x, y = position
        if x < 0 or x > 6 or y < self.cut:
            return True
        if y >= self.height:
            return False
        return self.a[y - self.cut][x]

    def __setitem__(self, position, value):
        x, y = position
        #print(f"Set {x} {y} on virtual height {self.height}, actual height {len(self.a)}.")

        if y >= self.height:
            #print(f"{y} >= {self.height}, increasing virtual height to {y + 1}.")
            self.a += [[0] * 7 for i in range(self.height, y+1)]
            self.height = y + 1
            #print(f"Virtual height increased to {self.height}, actual height increased to {len(self.a)}.")
        try:
            self.a[y - self.cut][x] = value
        except IndexError:
            raise IndexError(f"Trying to place {value} into ({x}, {y}) -> ({x}, {y - self.cut}) on grid of actual height {len(self.a)} and virtual height {self.height} with cut {self.cut}.")
        self.heights[x] = max(self.heights[x], y)

    def __repr__(self):
        return str(self) + f"\n{self.cut} rows hidden."

    def __str__(self):
        return "\n".join("".join(".#"[cell] for cell in row) for row in self.a[::-1])


def solve1(data):
    #lines = data.split("\n")
    shapes = get_shapes()
    wind = [{'<':-1, '>':1}[x] for x in data]
    def wind_fn(x={'time': 0}):
        w, x['time'] = wind[x['time']], (x['time'] + 1) % len(wind)
        return w
    grid = Grid()
    for i in range(2022):
        simulate_rock(grid, shapes[i % len(shapes)], wind_fn)
        grid.recut()
    print(repr(grid))
    return grid.height

def lcm(a,b):
    return a * b // gcd(a,b)

def gcd(a,b):
    if a < b:
        return gcd(b, a)
    while b:
        a, b = b, a % b
    return a

def solve2(data):
    shapes = get_shapes()
    wind = [{'<': -1, '>': 1}[x] for x in data]
    print(len(wind), len(shapes))
    period = lcm(len(shapes), len(wind))
    print(f"Period = {period}")
    def wind_fn(x={'time': 0}):
        w, x['time'] = wind[x['time']], (x['time'] + 1) % len(wind)
        return w
    grid = Grid()
    i = 0
    cache = {}
    limit = 10**12
    while i + period < limit:
        current = str(grid)
        print(i, len(cache))
        if current not in cache:
            h = grid.height
            for i2 in range(i, i + period):
                simulate_rock(grid, shapes[i2 % len(shapes)], wind_fn)
                grid.recut()
            cache[current] = (list(map(list, grid.a)), grid.height - h, i, len(cache))
            i += period
            print(repr(grid))
        else:
            print("Cycle found")
            h = grid.height
            cycle_length, cycle_height = cycle_search(cache, current)
            cycle_length *= period
            cycles = (limit - i) // cycle_length
            print(f"Cycle of length {cycle_length} and growth {cycle_height} fitting {cycles} up to {limit}.")

            h += cycles * cycle_height
            i += cycles * cycle_length
            grid = Grid(grid.a, h)
            print(i)
            break
    for i2 in range(i, limit):
        print(i2, grid.height)
        simulate_rock(grid, shapes[i2 % len(shapes)], wind_fn)
        grid.recut()

        #print(repr(grid))

    print(repr(grid), grid.height)

def cycle_search(cache, start):
    current = start
    i = 1
    height = 0
    print(current)
    while True:
        print(f"Cycling {i} {current}", cache[current])
        #print("\n\n\n".join(cache.keys()))
        #print(cache[current])
        #print(cache[current][0])
        current = str(Grid(cache[current][0]))
        height += cache[current][1]
        if current == start:
            break
        i += 1


    return i, height

def simulate_rock(grid: Grid, shape, wind):
    position = [2, grid.height + 3]
    for i in range(0, position[1] + 2):
        push = wind()
        if not collide(shape, grid, position, (push, 0)):
            position[0] += push
        if collide(shape, grid, position, (0, -1)):
            implant(shape, grid, position)
            break
        else:
            position[1] -= 1

def implant(shape, grid: Grid, position):
    for y,row in enumerate(shape):
        for x,cell in enumerate(row):
            if cell:
                grid[position[0] + x, position[1] + y] = 1



def collide(shape, grid: Grid, position, vector):
    for y,row in enumerate(shape):
        for x,cell in enumerate(row):
            new_pos = (position[0] + vector[0] + x, position[1] + vector[1] + y)
            if cell and grid[new_pos]:
                return True
    return False




def read_shape(s):
    return [[{'.':0,'#':1}[x] for x in line] for line in s.strip().split()][::-1]


def get_shapes():
    shapes = [
        '####',
        """

        .#.
        ###
        .#.

        """,
        """

        ..#
        ..#
        ###

        """,
        """

        #
        #
        #
        #

        """,
        """

        ##
        ##

        """
    ]
    return list(map(read_shape, shapes))




data = sys.stdin.read().strip()

#print(solve1(data))
print(solve2(data))