import sys

x = (s.split() for s in sys.stdin.read().strip().split("\n"))
directions = {'forward': 0, 'down': 0, 'up': 0}
for c, d in x:
    directions[c] += d

print(directions['forward'] * (directions['down'] - directions['up']))