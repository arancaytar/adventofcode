import sys

x = sys.stdin.read().strip().split()

y = [int(2*sum(map(int, c)) > len(c)) for c in zip(*x)]
z = int("".join(map(str, y)), 2) * int("".join(str(1-c) for c in y), 2)

print(z)