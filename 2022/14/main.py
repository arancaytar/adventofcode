import sys
import numpy as np

def read_path(s):
    points = [tuple(map(int, x.split(','))) for x in s.split(" -> ")]
    return points

class SparseMatrix:
    def __init(self):
        self.gri

def solve1(data):
    lines = data.split("\n")
    paths = [read_path(line) for line in lines]
    min_x = min(x for path in paths for x,y in path)
    min_y = min(y for path in paths for x,y in path)

    max_x = max(x for path in paths for x,y in path)
    max_y = max(y for path in paths for x,y in path)
    width = max_x - min_x
    height = max_y - min_y
    grid = np.zeros((max_y+1, max_x-min_x+1), dtype=int)

    for path in paths:
        for i in range(1, len(path)):
            x1,y1 = path[i-1]
            x2,y2 = path[i]
            x1,x2 = sorted((x1-min_x,x2-min_x))
            y1,y2 = sorted((y1,y2))
            grid[y1:y2+1,x1:x2+1] = 1
    draw(grid)

    for i in range(width*max_y):
        x,y = 500 - min_x, 0
        #print(x,y)
        rest = False
        while 0 <= x <= width and y < max_y:
            if not grid[y+1,x]:
                y += 1
            elif not grid[y+1,x-1]:
                x -= 1
                y += 1
            elif not grid[y+1,x+1]:
                x += 1
                y += 1
            else:
                grid[y,x] = 2
                rest = True
                break
            #print(x, y)
        #draw(grid)
        if not rest:
            return i

def draw(grid):
    height,width = grid.shape
    def drawrow(row):
        return "".join('.#o'[x] for x in row)
    print("\n".join(drawrow(grid[i,:]) for i in range(height)))

def solve2(data):
    lines = data.split("\n")
    paths = [read_path(line) for line in lines]
    min_x = min(x for path in paths for x,y in path)
    min_y = min(y for path in paths for x,y in path)

    max_x = max(x for path in paths for x,y in path)
    max_y = max(y for path in paths for x,y in path)
    width = max_x - min_x
    height = max_y - min_y
    #grid = np.zeros((max_y+3, max_x+2*max_y), dtype=int)
    grid = {}

    for path in paths:
        for i in range(1, len(path)):
            x1,y1 = path[i-1]
            x2,y2 = path[i]
            x1,x2 = sorted((x1,x2))
            y1,y2 = sorted((y1,y2))
            for i in range(x1,x2+1):
                for j in range(y1,y2+1):
                    grid[(i,j)] = 1

    i = 0
    while True:
        x,y = 500, 0
        rest = False
        while y < max_y + 1:
            if not (x,y+1) in grid:
                y += 1
            elif not (x-1,y+1) in grid:
                x -= 1
                y += 1
            elif not (x+1,y+1) in grid:
                x += 1
                y += 1
            else:
                grid[(x,y)] = 2
                break
        else:
            grid[(x,y)] = 2
        i += 1
        #draw2(grid)
        if (500,0) in grid:
            return i


def draw2(grid):
    min_x = 10**10
    max_x = -10**10
    min_y = 10**10
    max_y = -10**10
    for x,y in grid:
        min_x = min(min_x, x)
        max_x = max(max_x, x)
        min_y = min(min_y, y)
        max_y = max(max_y, y)
    width = max_x - min_x
    height = max_y - min_y
    rgrid = np.zeros((height+1,width+1), dtype=int)
    for x,y in grid:
        rgrid[y-min_y,x-min_x] = grid[x,y]
    draw(rgrid)
class infinite_grid:
    def __init(self, height, width):
        self.grid = np.zeros((height, width), dtype=int)
        self.zero = (0,0)

data = sys.stdin.read().strip()

print(solve1(data))
print(solve2(data))