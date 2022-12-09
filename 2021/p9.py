import sys

lines = sys.stdin.read().strip().split("\n")

lines2 = []
n = 0
for line in lines:
    start, end = line.split(" -> ")
    (a, b), (c, d) = start.split(","), end.split(",")
    a,b,c,d = tuple(map(int, (a,b,c,d)))
    lines2.append((a,b,c,d))
    n = max(n,a,b,c,d)

board = [[0]*(n+1) for i in range(n+1)]

for a,b,c,d in lines2:
    a,b,c,d = min(a,c), min(b,d), max(a,c), max(b,d)
    if a == c:
        for y in range(b, d+1):
            board[y][a] += 1
    elif b == d:
        for x in range(a, c+1):
            board[b][x] += 1

#for row in board:
#    print(row)
print(sum(x > 1 for row in board for x in row))