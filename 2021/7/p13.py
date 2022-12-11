x = sorted(list(map(int, input().split(","))))
median = x[len(x)//2]
print(sum(abs(c - median) for c in x))