import sys
import typing
def read() -> (list[range], list[int]):
    fresh, available = sys.stdin.read().strip().split("\n\n")
    fresh = [range(a, b+1) for a,b in (map(int, x.split("-")) for x in fresh.split())]
    available = list(map(int, available.split()))
    return fresh, available

def solve1(fresh: typing.Iterable[range], available: typing.Iterable[int]) -> int:
    return sum(any(x in range for range in fresh) for x in available)

def solve2(fresh: typing.Iterable[range]) -> int:
    s = 0
    fresh = sorted(fresh, key=lambda r:r.start) # sort range by start
    current = fresh[0]
    for r in fresh[1:]:
        if r.start < current.stop:
            current = range(current.start, max(r.stop, current.stop))
        else:
            s += len(current)
            current = r
    s += len(current)
    return s

def main():
    f, a = read()
    print(solve1(f, a))
    print(solve2(f))

main()