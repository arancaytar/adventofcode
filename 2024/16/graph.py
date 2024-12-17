import heapq

def bellman_ford_moore(graph, start, distance, predecessor=None):
    distance[start] = 0
    
    relax = {start}
    if predecessor is None:
        predecessor = {}
    predecessor[start] = None    
    while relax:
        new_relax = set()
        for u in relax:
            for v, w in graph.outgoing(u):
                new_dist = w + distance[u]
                if new_dist < distance[v]:
                    distance[v] = new_dist
                    predecessor[v] = {u}
                    new_relax.add(v)
                elif new_dist == distance[v]:
                    predecessor[v].add(u)
        relax = new_relax
    return distance, predecessor

def dijkstra(graph, start, distance, predecessor=None):
    distance[start] = 0
    
    Q = [(0, start)]
    heapq.heapify(Q)
    
    if predecessor is None:
        predecessor = {}
    predecessor[start] = None    
    
    while Q:
        d, u = heapq.heappop(Q)
        if distance[u] < d: # skip duplicates
            continue
        for v, w in graph.outgoing(u):
            new_dist = w + d
            if new_dist < distance[v]:
                distance[v] = new_dist
                heapq.heappush(Q, (new_dist, v))
                predecessor[v] = {u}
            elif new_dist == distance[v]:
                predecessor[v].add(u)
    return distance, predecessor


class DGraph:
      
    def outgoing(u):
        pass