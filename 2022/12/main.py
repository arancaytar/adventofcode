import collections
import sys
import numpy as np
import heapq

def read_matrix(data):
    lines = data.split("\n")
    matrix = np.matrix([list(map(rchr, line)) for line in lines],dtype=int)
    start = (0,0)
    end = (0,0)
    for y,line in enumerate(lines):
        for x,c in enumerate(line):
            if c == 'S':
                start = y,x
            if c == 'E':
                end = y,x
    return matrix, start, end

def solve1(data):
    matrix, start, end = read_matrix(data)
    height, width = matrix.shape

    best = np.ones(matrix.shape,dtype=int) * (height * width + 1)
    #dijkstra(best, neighbor_function(matrix), start)
    bfs(best, neighbor_function(matrix), start)

    return best[end]

def neighbor_function(matrix):
    h,w = matrix.shape
    def neighbors(coord):
        y,x = coord
        cur = matrix[coord]
        if x > 0 and (matrix[y,x - 1] - cur) <= 1:
            yield (y,x - 1), 1
        if y > 0 and (matrix[y-1,x] - cur) <= 1:
            yield (y - 1,x), 1
        if x + 1 < w and (matrix[y,x + 1] - cur) <= 1:
            yield (y, x + 1), 1
        if y + 1 < h and (matrix[y + 1,x] - cur) <= 1:
            yield (y + 1, x), 1
    return neighbors


def dijkstra(best, adjacency, source):
    queue = [(0, source)]
    heapq.heapify(queue)

    while queue:
        (best_u, u) = heapq.heappop(queue)
        if best[u] <= best_u:
            continue
        best[u] = best_u
        for v, edge in adjacency(u):
            heapq.heappush(queue, (best_u + edge, v))

def bfs(best, adjacency, source):
    queue = collections.deque([(0, source)])

    while queue:
        (best_u, u) = queue.popleft()
        if best[u] <= best_u:
            continue
        best[u] = best_u
        for v, _ in adjacency(u):
            queue.append((best_u + 1, v))


def rchr(letter):
    if letter == 'S':
        letter = 'a'
    elif letter == 'E':
        letter = 'z'
    return ord(letter) - ord('a')


def solve2(data):
    matrix, start, end = read_matrix(data)
    height, width = matrix.shape

    best = np.ones((height+1,width), dtype=int) * (height*width+1)
    start = (height, 0)

    starts = set()
    for y in range(height):
        for x in range(width):
            if matrix[y,x] == 0:
                starts.add((y,x))

    #dijkstra(best, multisource(neighbor_function(matrix), starts, start), start)
    bfs(best, multisource(neighbor_function(matrix), starts, start), start)

    return best[end] - 1

def multisource(adjacency, sources, source):
    def adjacency_(coord):
        if coord == source:
            yield from ((s, 0) for s in sources)
        else:
            yield from adjacency(coord)
    return adjacency_

data = sys.stdin.read().strip()

print(solve1(data))
print(solve2(data))