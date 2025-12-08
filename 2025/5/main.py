import sys

def read():
    fresh, available = sys.stdin.read().strip().split("\n\n")
    fresh = [tuple(map(int, x.split("-"))) for x in fresh.split()]
    available = list(map(int, available.split()))
    return fresh, available
def solve1(fresh, available):
    fresh = [range(a, b + 1) for a, b in fresh]
    return sum(any(x in range for range in fresh) for x in available)

def solve2(fresh):
    fresh_unique = {}
    for a, b in fresh:
        if a not in fresh_unique:
            fresh_unique[a] = b
        fresh_unique[a] = max(fresh_unique[a], b)
    latest_start = 0
    latest = 0
    for a in sorted(fresh_unique.keys()):
        #print(f"[{latest_start}-{latest}]: Range {a}-{fresh_unique[a]}")
        # if our range starts inside the last open range, extend it to the end
        if a <= latest:
            fresh_unique[latest_start] = latest = max(fresh_unique[a], latest)
            # delete the redundant range
            fresh_unique[a] = None
        else:
            latest_start, latest = a, fresh_unique[a]
    #print(fresh_unique)
    # now all the ranges are disjoint.
    return sum(b - a + 1 for a, b in fresh_unique.items() if b is not None)


def main():
    f, a = read()
    print(solve1(f, a))
    print(solve2(f))

main()