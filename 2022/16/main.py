import sys
import numpy as np
import re
import collections
import ortools

class AdjList:
    def __init__(self):
        self.adj = {}
        self.weight = {}
    def addNode(self, u, weight, *v):
        self.adj[u] = list(v)
        self.weight[u] = weight

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

def solve1(data):
    adj, weights = read_graph(data)

    max_flow = {('AA', frozenset()): 0}
    for i in range(30):
        print(i, len(max_flow))
        max_flow_new = collections.defaultdict(int)
        for key, m in max_flow.items():
            u, opened = key
            idle = sum(weights[x] for x in opened)

            max_flow_new[key] = max(
                max_flow_new[key],
                m + idle
            )

            #try opening the valve
            if u not in opened and weights[u]:
                add_u = (u, opened | frozenset({u}))
                max_flow_new[add_u] = max(
                    max_flow_new[add_u],
                    max_flow[key] + idle
                )

            #try moving elsewhere
            for v in adj[u]:
                move_v = (v, opened)
                max_flow_new[move_v] = max(
                    max_flow_new[move_v],
                    max_flow[key] + idle
                )
        max_flow = max_flow_new

    return max((v, k) for k, v in max_flow.items())
    #return max(max_flow.values())

def solve12(data):
    adj, weights = read_graph(data)

    max_flow = {('AA', frozenset()): 0}
    for i in range(30):

        max_flow_new = collections.defaultdict(int)
        for key, m in max_flow.items():
            u, opened = key
            idle = sum(weights[x] for x in opened)

            max_flow_new[key] = max(
                max_flow_new[key],
                m + idle
            )

            #try opening the valve
            if u not in opened and weights[u]:
                add_u = (u, opened | frozenset({u}))
                max_flow_new[add_u] = max(
                    max_flow_new[add_u],
                    max_flow[key] + idle
                )

            #try moving elsewhere
            for v in adj[u]:
                move_v = (v, opened)
                max_flow_new[move_v] = max(
                    max_flow_new[move_v],
                    max_flow[key] + idle
                )
        max_flow = max_flow_new

    return max((v,k) for k,v in max_flow.items())

def solve2(data):
    adj, weights = read_graph(data)

    max_flow = {(frozenset({'AA'})): (0, set(), ())}
    limit = 26
    for i in range(limit):
        print(i, len(max_flow))
        max_flow_new = collections.defaultdict(lambda: (-1, set(), ()))
        for key, val in max_flow.items():
            #print(key, val)
            if len(key) == 1:
                u1, u2 = list(key)*2
            else:
                u1, u2 = key
            opt, opened, history = val
            #debug(i, max_flow_new)
            #try opening both valves
            if u1 != u2 and not {u1, u2} & opened and weights[u1] * weights[u2]:
                new_opt = opt + (weights[u1] + weights[u2]) * (limit - i - 1)
                if new_opt > max_flow_new[key][0]:
                    max_flow_new[key] = new_opt, opened | {u1, u2}, (f'open {u1} {u2} {new_opt}', key, history)
            #try opening one and moving from the other.
            #debug(i, max_flow_new)
            if u1 not in opened and weights[u1]:
                new_opt = opt + weights[u1] * (limit - i - 1)
                for v2 in adj[u2]:
                    new_key = frozenset({u1, v2})
                    if new_opt > max_flow_new[new_key][0]:
                        max_flow_new[new_key] = new_opt, opened | {u1}, (f'open {u1} move {u2}->{v2} {new_opt}', key, history)
            #debug(i, max_flow_new)
            if u2 not in opened and weights[u2]:
                new_opt = opt + weights[u2] * (limit - i - 1)
                for v1 in adj[u1]:
                    new_key = frozenset({v1, u2})
                    if new_opt > max_flow_new[new_key][0]:
                        max_flow_new[new_key] = new_opt, opened | {u2}, (f'open {u2} move {u1}->{v1} {new_opt}', key, history)
            #debug(i, max_flow_new)
            #try moving both.
            new_keys = {frozenset({v1, v2}) for v1 in adj[u1] for v2 in adj[u2]}
            for new_key in new_keys:
                if opt > max_flow_new[new_key][0]:
                    max_flow_new[new_key] = opt, opened, (f'move {new_key} {opt}', key, history)

        debug(i, max_flow_new)
        #print(max_flow_new)
        max_flow = max_flow_new
        print(max(max_flow.values()))

    return max(max_flow.values())

def solve21(data):
    adj, weights = read_graph(data)
    mf_human = solve21_(adj, weights)
    score,(position,opened) = max((v,k) for k,v in mf_human.items())
    weights2 = {x:y * (x not in opened) for x,y in weights.items()}
    mf_ele = solve21_(adj, weights2)
    return (score, max(mf_ele.values()), score + max(mf_ele.values()))

def solve21_(adj, weights):
    max_flow = {('AA', frozenset()): 0}
    for i in range(26):
        max_flow_new = collections.defaultdict(int)
        for key, m in max_flow.items():
            u, opened = key
            idle = sum(weights[x] for x in opened)

            max_flow_new[key] = max(
                max_flow_new[key],
                m + idle
            )

            #try opening the valve
            if u not in opened and weights[u]:
                add_u = (u, opened | frozenset({u}))
                max_flow_new[add_u] = max(
                    max_flow_new[add_u],
                    max_flow[key] + idle
                )

            #try moving elsewhere
            for v in adj[u]:
                move_v = (v, opened)
                max_flow_new[move_v] = max(
                    max_flow_new[move_v],
                    max_flow[key] + idle
                )
        max_flow = max_flow_new

    return max_flow

def solve21_b(data):
    adj, weights = read_graph(data)

    max_flow = {'AA': (0, set())}
    limit = 30
    for i in range(limit):
        print(i, len(max_flow))
        max_flow_new = collections.defaultdict(lambda: (-1, set()))
        for u, val in max_flow.items():
            #print(key, val)
            opt, opened = val
            #debug(i, max_flow_new)
            if u not in opened and weights[u]:
                new_opt = opt + weights[u] * (limit - i - 1)
                if new_opt > max_flow_new[u][0]:
                    max_flow_new[u] = new_opt, opened | {u}
            #debug(i, max_flow_new)
            for v in adj[u]:
                if opt > max_flow_new[v][0]:
                    max_flow_new[v] = opt, opened

        debug(i, max_flow_new)
        #print(max_flow_new)
        max_flow = max_flow_new
        print(max(max_flow.values()))

    return max(max_flow.values())

def solve23(data):
    adj, weights = read_graph(data)

    max_flow = {(frozenset({'AA'}), frozenset()): 0}
    limit = 16
    idle = {}
    for i in range(limit):
        max_flow_new = collections.defaultdict(lambda: -1)
        for (position, opened), val in max_flow.items():
            if opened not in idle:
                idle[opened] = sum(weights[x] for x in opened)
            new_val = val + idle[opened]
            #print(key, val)
            if len(position) == 1:
                u1, u2 = list(position)*2
            else:
                u1, u2 = position

            #debug(i, max_flow_new)
            #try opening both valves
            if u1 != u2 and not {u1, u2} & opened and weights[u1] * weights[u2]:
                new_key = position, opened | frozenset({u1, u2})
                max_flow_new[new_key] = max(max_flow_new[new_key], new_val)
            #try opening one and moving from the other.
            #debug(i, max_flow_new)
            if u1 not in opened and weights[u1]:
                for v2 in adj[u2]:
                    new_key = frozenset({u1, v2}), opened | frozenset({u1})
                    max_flow_new[new_key] = max(max_flow_new[new_key], new_val)
            #debug(i, max_flow_new)
            if u2 not in opened and weights[u2]:
                for v1 in adj[u1]:
                    new_key = frozenset({v1, u2}), opened | frozenset({u2})
                    max_flow_new[new_key] = max(max_flow_new[new_key], new_val)
            #debug(i, max_flow_new)
            #try moving both.
            new_positions = {frozenset({v1, v2}) for v1 in adj[u1] for v2 in adj[u2]}
            for new_position in new_positions:
                new_key = (new_position, opened)
                max_flow_new[new_key] = max(max_flow_new[new_key], new_val)

        #debug(i, max_flow_new)
        #print(max_flow_new)
        max_flow = max_flow_new
        print(max(max_flow.values()))

    return max(max_flow.values())

data = sys.stdin.read().strip()
def debug(i, max_flow_new):
    return
    if i == 0:
        print('step', i, 'II/DD', max_flow_new[frozenset({'II', 'DD'})])
    if i == 1:
        print('step', i, 'JJ/DD', max_flow_new[frozenset({'JJ', 'DD'})])
    if i == 2:
        print('step', i, 'JJ/EE', max_flow_new[frozenset({'JJ', 'EE'})])
    if i == 3:
        print('step', i, 'II/FF', max_flow_new[frozenset({'II', 'FF'})])
    if i == 4:
        print('step', i, 'AA/GG', max_flow_new[frozenset({'AA', 'GG'})])
        print('step', i, 'BB/HH', max_flow_new[frozenset({'BB', 'HH'})])
    if i == 5:
        print('step', i, 'BB/HH', max_flow_new[frozenset({'BB', 'HH'})])
#print(solve1(data))
print(solve23(data))