import sys
import functools

def solve1(data):
    line_pairs = data.split("\n\n")
    line_pairs = [x.split("\n") for x in line_pairs]
    line_pairs = [[eval(x) for x in y] for y in line_pairs]
    s = 0
    for i,(a,b) in enumerate(line_pairs):
        c = compare(a, b)
        if c < 0:
            s += i + 1

    return s

def compare(a, b):
    if type(a) == int and type(b) == int:
        if a < b:
            return -1
        elif a > b:
            return 1
    elif type(a) == list and type(b) == list:
        for x,y in zip(a, b):
            c = compare(x, y)
            if c != 0:
                return c
        if len(a) < len(b):
            return -1
        elif len(a) > len(b):
            return 1
    elif type(a) == int and type(b) == list:
        return compare([a], b)
    elif type(b) == int and type(a) == list:
        return compare(a, [b])

    return 0

def solve2(data):
    lines = [eval(x) for x in data.split("\n") if x] + [[[2]], [[6]]]
    lines = sorted(lines, key=functools.cmp_to_key(compare))
    a,b = None,None
    for i,s in enumerate(lines):
        if s == [[2]]:
            a = i + 1
        elif s == [[6]]:
            b = i + 1
    return a*b


data = sys.stdin.read().strip()

print(solve1(data))
print(solve2(data))