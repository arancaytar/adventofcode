import sys
elves = [sum(map(int, x.split())) for x in  sys.stdin.read().split("\n\n")]

elves = sorted(elves, reverse=True)

print(elves[0])
print(sum(elves[:3]))


