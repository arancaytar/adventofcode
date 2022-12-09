import sys
solution = None

def s1(line):
    a,b = line.split(",")
    a1,a2 = map(int, a.split("-"))
    b1, b2 = map(int, b.split("-"))
    return (
            (a1 <= b1) and (a2 >= b2)
            or
            (a1 >= b1) and (a2 <= b2))

def solve1(data):
    lines = data.split()
    return sum(map(s1, lines))
def s2(line):
    a,b = line.split(",")
    a1,a2 = map(int, a.split("-"))
    b1, b2 = map(int, b.split("-"))
    return not ((a2 < b1) or (a1 > b2))

def solve2(data):
    lines = data.split()
    return sum(map(s2, lines))
    return solution

data = sys.stdin.read()

print(solve1(data))
print(solve2(data))