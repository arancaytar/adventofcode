import sys

def process(s):
    n = len(s)//2
    a,b = s[:n], s[n:]
    t = list(set(a) & set(b))[0]
    print(t)

def pri(t):
    if 'a' <= t <= 'z':
        return ord(t) - ord('a') + 1
    else:
        return ord(t) - ord('A') + 27


def main():
    lines = sys.stdin.read().split()
    r = [process(line) for line in lines]
    print(r)
    return sum(r)

    pass

def process2(t):
    a, b, c = map(set, t)
    badge = list(a & b & c)[0]
    return pri(badge)

def main2():
    lines = sys.stdin.read().split()
    triples = [lines[i:i + 3] for i in range(0, len(lines), 3)]
    r = [process2(t) for t in triples]
    return sum(r)
print(main2())