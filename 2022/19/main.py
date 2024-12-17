import sys
import numpy as np
import re
import collections
import math
def read_bp(data):
    bp = {}
    data = data.split(":")[1].strip()
    for line in data.split("."):
        m = re.match('.*Each (.+) robot costs (\d+) ore( and (\d+) (.+))?', line.strip())
        if m:
            x = m.group(1)
            bp[x] = {'ore': int(m.group(2))}
            if m.group(3):
                bp[x][m.group(5)] = int(m.group(4))
    return bp

def solve1(data):
    bps = map(read_bp, data.split("\n"))
    limit = 24
    return sum(i * optimize(b, limit) for i, b in enumerate(bps, start=1))

#    g1 = optimize(bp2, 24)
 #   return g1
    #g2 = optimize(bp2, 20)

def optimize(bp, limit):
    current = {((0, 0, 1), (0, 0, 0)): 0}
    max_costs = {x:max([z[x] for z in bp.values() if x in z]+[0]) for x in bp}

    for i in range(limit):
        print(i, len(current))
        succ = collections.defaultdict(int)
        for state, geodes in current.items():
            (o, c, r), (obsidian, clay, ore) = state
            obsidian2, clay2, ore2 = obsidian + o, clay + c, ore + r
            if obsidian >= bp['geode']['obsidian'] and ore >= bp['geode']['ore']:
                s1 = (o, c, r), (obsidian2 - bp['geode']['obsidian'], clay2, ore2 - bp['geode']['ore'])
                succ[s1] = max(succ[s1], geodes + (limit - i - 1))
                continue
            if o < max_costs['obsidian'] and clay >= bp['obsidian']['clay'] and ore >= bp['obsidian']['ore']:
                s1 = (o+1, c, r), (obsidian2, clay2 - bp['obsidian']['clay'], ore2 - bp['obsidian']['ore'])
                succ[s1] = max(succ[s1], geodes)
            if c < max_costs['clay'] and ore >= bp['clay']['ore']:
                s1 = (o, c+1, r), (obsidian2, clay2, ore2 - bp['clay']['ore'])
                succ[s1] = max(succ[s1], geodes)
            if r < max_costs['ore'] and ore >= bp['ore']['ore']:
                s1 = (o, c, r+1), (obsidian2, clay2, ore2 - bp['ore']['ore'])
                succ[s1] = max(succ[s1], geodes)
            s1 = (o, c, r), (obsidian2, clay2, ore2)
            succ[s1] = max(succ[s1], geodes)
        current = succ
    return max(current.values())

def solve2(data):
    bps = list(map(read_bp, data.split("\n")))[:3]
    limit = 32
    return math.prod(optimize(b, limit) for i, b in enumerate(bps, start=1))


data = sys.stdin.read().strip()

#print(solve1(data))
print(solve2(data))