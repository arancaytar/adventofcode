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
    paths['start'][frozenset()] = 1
    Q = deque()
    Q.append(('start', frozenset()))
    while Q:
        node, subset = Q.popleft()
        # no paths can keep going after the end
        if node == 'end':
            continue
        #print(f"In {node} having visited {subset} over {paths[node][subset]} paths")
        affected = set()
        new_subset = subset | {node} if node.upper() != node else subset
        # any unvisited neighbor
        for neighbor in adj[node] - subset:
            if new_subset not in paths[neighbor]:
                paths[neighbor][new_subset] = 0
            #print(f"    Adding to {neighbor} : {new_subset} -> {paths[neighbor][new_subset]}")
            paths[neighbor][new_subset] += paths[node][subset]
            #print(f"         {paths[neighbor][new_subset]}")
            Q.append((neighbor, new_subset))
        paths[node][subset] = 0
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
