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
    n, m = len(matrix), len(matrix[0])
    def neighbor(idx):
        i, j = idx
        for di in -1, 1:
            i2 = i + di
            if 0 <= i2 < n:
                yield (i2, j), matrix[i2][j]
        for dj in -1, 1:
            j2 = j + dj
            if 0 <= j2 < m:
                yield (i, j2), matrix[i][j2]
    return neighbor

def solve(matrix):
    paths = dijkstra(matrixgraph(matrix), (0, 0))
    n, m = len(matrix), len(matrix[0])
    return paths[(n - 1, m - 1)]

print(solve(read()))