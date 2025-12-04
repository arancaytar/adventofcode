import numpy as np
import grid
import sys
from collections import deque

def read():
    #return [[c == '@' for c in line] for line in sys.stdin.read().strip().split()]
    return grid.Grid.read(sys.stdin.read(), {'.': False, '@': True})

def solve1(g):
    return sum(sum(c for _, c in g.neighbors8(x, y)) < 4 for (x,y), c in g if c)

def solve2(g):
    g2 = grid.Grid(np.zeros(g.shape))
    q = deque()
    for (x, y), c in g:
        if c:
            g2[x, y] = sum(c for _, c in g.neighbors8(x, y))
            if g2[x, y] < 4:
                q.append((x, y))

    removed = 0
    while q:
        x, y = q.popleft()
        if not g[x, y]:
            continue
        g[x, y] = False
        removed += 1
        for (x2, y2), c in g.neighbors8(x, y):
            if c:
                g2[x2, y2] -= 1
                if g2[x2, y2] < 4:
                    q.append((x2, y2))
    return removed

def main():
    g = read()
    print(solve1(g))
    print(solve2(g))

main()