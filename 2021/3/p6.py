import sys

x = sys.stdin.read().strip().split()
y = set(x)
z = set(x)
for i in range(len(x[0])):
    if len(y) > 1:
        bit = 2*sum(int(c[i]) for c in y) >= len(y)
        y = set(filter(lambda c: int(c[i]) == bit, y))
    if len(z) > 1:
        bit2 = 2 * sum(int(c[i]) for c in z) >= len(z)
        z = set(filter(lambda c: int(c[i]) != bit2, z))

print(int(list(y)[0], 2) * int(list(z)[0], 2))