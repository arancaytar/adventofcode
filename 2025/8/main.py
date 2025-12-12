import sys
from collections import Counter
import math

def read():
    return [tuple(map(int, l.split(","))) for l in sys.stdin.read().strip().split("\n")], int(sys.argv[1])

class UF:
    def __init__(self, x):
        self.idx = {c: c for c in x}

    def find(self, x):
        if self.idx[x] == x:
            return x
        else:
            self.idx[x] = self.find(self.idx[x])
            return self.idx[x]

    def merge(self, a, b):
        a, b = self.find(a), self.find(b)
        a, b = sorted([a, b])
        if self.idx[b] != a:
            self.idx[b] = a
            return True
        return False

def dist(p1, p2):
    return sum((c1 - c2)**2 for c1, c2 in zip(p1, p2))**0.5

def solve1(coords, k):
    n = len(coords)
    pairs = sorted(((coords[i], coords[j]) for i in range(0, n) for j in range(i+1, n)), key=lambda p: dist(*p))[:k]

    x = UF(coords)
    for p1, p2 in pairs:
        x.merge(p1, p2)
    sizes = sorted(Counter(x.find(p) for p in coords).values(), reverse=True)[:3]
    return math.prod(sizes)

def solve2(coords):
    n = len(coords)
    pairs = sorted(((coords[i], coords[j]) for i in range(0, n) for j in range(i+1, n)), key=lambda p: dist(*p))

    x = UF(coords)
    k = n
    for p1, p2 in pairs:
        k -= x.merge(p1, p2)
        if k == 1:
            return p1[0] * p2[0]

def main():
    coords, k = read()
    print(solve1(coords, k))
    print(solve2(coords))
def solve3(coords):
    idx = {
        'x': sorted(coords, key=lambda x: x[0]),
        'y': sorted(coords, key=lambda x: x[1]),
        'z': sorted(coords, key=lambda x: x[2])
    }
    ranks = {
        c: {coord: i for i, coord in enumerate(v)}
        for c,v in idx.items()
    }

    axis = {'x': 0, 'y': 1, 'z': 2}
    n = len(coords)
    def closest(coord):
        r = {c:ranks[c][coord] for c in ranks}
        max_dist = 1e64
        best = None
        for c in idx:
            for s1, s2 in ((-1, -1), (1, n)):
                for j in range(r + s1, s2, s1):
                    candidate = idx[c][j]
                    candidate_dist = dist(candidate, coord)
                    if candidate_dist < max_dist:
                        best = candidate
                        max_dist = candidate_dist
                    min_dist = abs(candidate[axis[c]] - coord[axis[c]])
                    if min_dist >= max_dist:
                        break
        return best

main()