import sys
import re
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

adj, weights = read_graph(sys.stdin.read().strip())

def nodes(w):
    return "\n".join(f"node [label=\"{x},{y}\"]{x};" for x,y in w.items())

def edges(a):
    edges = {frozenset({u,v}) for u,vv in a.items() for v in vv}
    return "\n".join(f"{u} -- {v};" for u,v in edges)


print(f'graph {{{nodes(weights)}\n{edges(adj)}}}')