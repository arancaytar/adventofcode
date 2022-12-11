from collections import deque

def read_graph():
    adj = {}
    while True:
        try:
            u, v = input().split('-')
        except EOFError:
            break
        if u not in adj:
            adj[u] = set()
        if v not in adj:
            adj[v] = set()
        adj[u].add(v)
        adj[v].add(u)
    return adj

def bfs(adj):
    paths = {node: {} for node in adj}
    paths['start'][frozenset(), None] = 1
    Q = deque()
    Q.append(('start', frozenset(), None))
    while Q:
        node, subset, duplicate = Q.popleft()
        # no paths can keep going after the end
        if node == 'end':
            continue

        # if we visited this node already, duplicate it.
        new_duplicate = node if node in subset else duplicate
        # otherwise, add it
        new_subset = subset | {node} if node.upper() != node else subset

        # any unvisited neighbor
        neighbors = adj[node] - {'start'}
        # if we already duplicated a node, forbid any others
        if new_duplicate:
            neighbors -= subset
        for neighbor in neighbors:
            if (new_subset, new_duplicate) not in paths[neighbor]:
                paths[neighbor][new_subset, new_duplicate] = 0
            #print(f"    Adding to {neighbor} : {new_subset} -> {paths[neighbor][new_subset]}")
            paths[neighbor][new_subset, new_duplicate] += paths[node][subset, duplicate]
            #print(f"         {paths[neighbor][new_subset]}")
            Q.append((neighbor, new_subset, new_duplicate))
        paths[node][subset, duplicate] = 0
    #print(paths)
    return sum(paths['end'].values())

print(bfs(read_graph()))

def process_graph(adj):
    bignodes = {x for x in adj.keys() if x.upper() == x}

    # Transform any big node into a complete graph between all its neighbors.
    for node in bignodes:
        problem = adj[node] & bignodes
        if problem:
            raise ValueError(f"{node}-{problem} presents infinite distinct paths of arb length")
        for u in adj[node]:
            for v in adj[node]:
                if u != v:
                    adj[u].add(v)

    for node in adj:
        adj[node] -= bignodes
    return adj
