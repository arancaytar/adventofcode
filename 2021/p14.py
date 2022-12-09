x = sorted(list(map(int, input().split(","))))
mean = round(sum(x) / len(x))
print(mean)
for m in range(mean - 10, mean+10):
    dist = [abs(c - m) for c in x]
    print(sum(c*(c+1)//2 for c in dist))