import heapq
import sys
import re
def dijkstra(best, adjacency, source):
    queue = [(0, source)]
    heapq.heapify(queue)

    while queue:
        (best_u, u) = heapq.heappop(queue)
        if best[u] <= best_u:
            continue
        best[u] = best_u
        for v, edge in adjacency(u):
            heapq.heappush(queue, (best_u + edge, v))

def read_graph(data):
    lines = data.split("\n")

    adj = {}
    weights = {}
    for line in lines:
        m = re.match('Valve (..) has flow rate=(\d+); tunnels? leads? to valves? (.*)', line)
        u, weight, v = (m.group(i) for i in range(1, 4))
        adj[u] = v.split(", ")
        weights[u] = int(weight)
    return adj, weights

def normalize(adj, weights):
    adj2 = {}
    for x in weights:
        if weights[x] or x == 'AA':
            adj2[x] = {}
            dist = {x: len(adj) + 1 for x in weights}
            dijkstra(dist, (lambda u: ((v, 1) for v in adj[u])), x)
            for y in weights:
                if x!=y and (weights[y] or y == 'AA'):
                    adj2[x][y] = dist[y]
    return adj2


def solve(data):
    adj1, weights = read_graph(data)
    adj = normalize(adj1, weights)

    memo1 = {}
    def aggregate_(opened):
        o = frozenset(opened)
        if not o in memo1:
            memo1[o] = sum(weights[x] for x in opened)
        return memo1[o]

    memo2 = {}
    def solve_(location, remaining, opened):
        o = frozenset(opened)
        if (location, remaining, o) not in memo2:
            values = []
            if remaining <= 0:
                return 0
            if location not in opened:
                values.append(aggregate_(opened) + solve_(location, remaining - 1, opened | {location}))
            #for v,d in adj[location].items():
            for v in adj1[location]:
                d = 1
                values.append(aggregate_(opened) + solve_(v, remaining - d, opened))
            memo2[location, remaining, o] = max(values)
        return memo2[location, remaining, o]
    return solve_('AA', 30, set())

print(solve(sys.stdin.read().strip()))