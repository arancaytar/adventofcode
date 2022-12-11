import sys
import heapq
import typing
from collections import defaultdict

class inf:
    def __lt__(self, other):
        return False
    def __gt__(self, other):
        return True
    def __add__(self, other):
        return self
    def __repr__(self):
        return 'inf'

class RepMatrix:
    def __init__(self, matrix, rep: int):
        self._matrix = matrix
        self._shape = (len(matrix), len(matrix[0]))
        self._rep = rep

    def shape(self):
        return (self._shape[0] * self._rep, self._shape[1] * self._rep)

    def __getitem__(self, key):
        i, j = key
        r1, i = divmod(i, self._shape[0])
        r2, j = divmod(j, self._shape[0])
        if r1 >= self._rep or r2 >= self._rep:
            raise KeyError()
        return ((self._matrix[i][j] + r1 + r2) - 1) % 9 + 1
    def __str__(self):
        n, m = self.shape()
        return "\n".join("".join(str(self[i, j]) for j in range(m)) for i in range(n))

def dijkstra(neighbor_fn: typing.Callable, start):
    q = [(0, start)]
    path = defaultdict(lambda: (inf(), None), {start: (0, None)})
    heapq.heapify(q)
    while q:
        cost, u = heapq.heappop(q)
        if path[u][0] < cost:
            continue
        for v, edge_cost in neighbor_fn(u):
            new_cost = path[u][0] + edge_cost
            if new_cost < path[v][0]:
                path[v] = (new_cost, u)
                heapq.heappush(q, (path[v][0], v))
    return path

def read():
    return [list(map(int, r)) for r in sys.stdin.read().split("\n")]

def matrixgraph(matrix):
    n, m = matrix.shape()
    def neighbor(idx):
        i, j = idx
        for di in -1, 1:
            i2 = i + di
            if 0 <= i2 < n:
                yield (i2, j), matrix[i2, j]
        for dj in -1, 1:
            j2 = j + dj
            if 0 <= j2 < m:
                yield (i, j2), matrix[i, j2]
    return neighbor

def solve(matrix):
    matrix = RepMatrix(matrix, 5)
    #print(matrix)
    paths = dijkstra(matrixgraph(matrix), (0, 0))
    n, m = matrix.shape()
    return paths[(n - 1, m - 1)]

print(solve(read()))