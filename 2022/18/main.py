import sys
import numpy as np
def read_points(data):
    return list(tuple(map(int, x.split(','))) for x in data.split("\n"))

def solve1(data):
    points = set(read_points(data))
    return sum(6 - len({(x-1,y,z), (x+1,y,z), (x,y-1,z), (x,y+1,z), (x,y,z-1), (x,y,z+1)} & points) for x,y,z in points)

class SetUnion:
    def __init__(self, x: set):
        self.a = {y: y for y in x}

    def unify(self, a, b):
        if a < b:
            a, b = b, a
        self.a[self.find(a)] = self.find(b)

    def find(self, u):
        if self.a[u] != u:
            self.a[u] = self.find(self.a[u])
        return self.a[u]

    def normalize(self):
        for x in self.a:
            self.find(x)
        return set(self.a.values())

def neighbors(x,y,z):
    return {(x - 1, y, z), (x + 1, y, z), (x, y - 1, z), (x, y + 1, z), (x, y, z - 1), (x, y, z + 1)}

def flow(matrix, dimension):
    check_set = set.union(*(({(0, i, j), (dimension, i, j),
        (i, 0, j), (i, dimension, j),
        (i, j, 0), (i, j, dimension)}) for i in range(dimension+1) for j in range(dimension+1)))

    while check_set:
        check_set2 = set()
        for x,y,z in check_set:
            if valid(x,y,z,dimension) and matrix[x, y, z] == 0:
                matrix[x,y,z] = 2
                check_set2 |= neighbors(x,y,z)
        check_set = check_set2
    print(matrix)

def valid(x, y, z, dimension):
    return 0 <= min(x, y, z) and max(x, y, z) <= dimension

def solve2(data):
    points = set(read_points(data))
    #open_neighbors = {point: (neighbors(*point) - points) for point in points}
    #air_blocks = set.union(*open_neighbors.values())
    #print(len(air_blocks))
    #bubbles = SetUnion(air_blocks)
    #for point in air_blocks:
     #   for n in neighbors(*point) & air_blocks:
     #       print(point, n)
    #        bubbles.unify(point, n)
    #bubbles2 = bubbles.normalize()


    #for point in points:
    #    matrix[point] = 1
    #for i, bubble in enumerate(bubbles2):
    #    bfs(bubble, matrix)

    dimension = max(max(point) for point in points)
    matrix = np.zeros((dimension+1, dimension+1, dimension+1), dtype=int)
    for point in points:
        matrix[point] = 1
    flow(matrix, dimension)
    #print(matrix)
    #matrix2 = np.zeros((dimension + 1, dimension + 1, dimension + 1), dtype=int)
    #for p in points:
    #    matrix2[p] = -sum(valid(*n, dimension) and matrix[n] == 2 for n in neighbors(*p))
    #print(matrix2)
    return sum(sum(not valid(*n, dimension) or matrix[n] == 2 for n in neighbors(*p)) for p in points)
data = sys.stdin.read().strip()

#print(solve1(data))
print(solve2(data))