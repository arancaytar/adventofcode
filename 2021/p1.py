import sys

x = list(map(int, sys.stdin.read().strip().split()))
d = sum(x[i] > x[i-1] for i in range(1, len(x)))
print(d)
