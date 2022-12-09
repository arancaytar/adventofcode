import sys

x = list(map(int, sys.stdin.read().strip().split()))
s = [sum(x[i:i+3]) for i in range(len(x)-2)]
d = sum(s[i] > s[i-1] for i in range(1, len(s)))
print(d)
