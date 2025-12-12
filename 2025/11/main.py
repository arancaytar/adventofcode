import sys

def get_edges(outgoing):
    yield from ((a, b) for a, outputs in outgoing.items() for b in outputs)

def get_incoming(outgoing):
    inc = {}
    for a, b in get_edges(outgoing):
        if b not in inc:
            inc[b] = set()
        inc[b].add(a)
    return inc

def read():
    return {x[0][:-1]: tuple(x[1:]) for x in (x.split() for x in sys.stdin.read().strip().split("\n"))}
def solve1(devices):
    paths = {'you': 1}
    cur = {'you'}
    if 'you' not in devices:
        return 0
    for i in range(len(devices)):
        if not cur:
            break
        cur2 = set()
        for node in cur:
            if node in devices:
                for b in devices[node]:
                    if b not in paths:
                        paths[b] = 0
                    paths[b] += paths[node]
                    cur2.add(b)
                paths[node] = 0
        cur = cur2
    if cur:
        raise ValueError(f"Graph is not acyclic in the nodes {cur}")

    return paths['out']

def solve2(devices):
    paths = {'svr': [1, 0, 0, 0]}
    cur = {'svr'}
    for i in range(len(devices)):
        if not cur:
            break
        cur2 = set()
        for node in cur:
            if node in devices:
                for b in devices[node]:
                    if b not in paths:
                        paths[b] = [0, 0, 0, 0]
                    if b == 'dac':
                        paths[b] = [0, paths[b][1] + paths[node][0], 0, paths[b][3] + paths[node][2]]
                    elif b == 'fft':
                        paths[b] = [0, 0, paths[b][2] + paths[node][0], paths[b][3] + paths[node][1]]
                    else:
                        paths[b] = [a + b for a,b in zip(paths[b], paths[node])]
                    cur2.add(b)
                paths[node] = [0, 0, 0, 0]
        cur = cur2
    if cur:
        raise ValueError(f"Graph is not acyclic in the nodes {cur}")

    return paths['out']

# bad: 77039728955956024816575004
def main():
    d = read()
    print(solve1(d))
    print(solve2(d))

main()
