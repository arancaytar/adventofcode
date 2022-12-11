import sys

x = (s.split() for s in sys.stdin.read().strip().split("\n"))
directions = {'forward': 0, 'depth': 0, 'aim': 0}
for c, d in x:
    d = int(d)
    if c == 'forward':
        directions[c] += d
        directions['depth'] += d*directions['aim']
    else:
        directions['aim'] += (d if c == 'down' else -d)

print(directions['forward'] * directions['depth'])