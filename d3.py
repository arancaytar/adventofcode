import sys

def check(trees, right, down):
    x, y = 0, 0
    counter = 0
    while y < len(trees):
        counter += trees[y][x]
        y += down
        x = (x + right) % len(trees[0])
    return counter


def read():
    lines = sys.stdin.read().split("\n")
    return [[x == '#' for x in line] for line in lines]


def check2(trees):
    c = 1
    for x, y in [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]:
        d = check(trees, x, y)
        print(c, d)
        c *= d
    return c
print(check2(read()))