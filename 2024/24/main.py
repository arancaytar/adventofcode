from grid import Grid
from graph import dijkstra,DGraph
import sys
import numpy as np
from collections import Counter, deque
from itertools import islice
import re

def read():
    values,connections = sys.stdin.read().strip().split("\n\n")
    values = [re.match(r"(...): (0|1)", line) for line in values.split("\n")]
    connections = [re.match(r"(...) (AND|OR|XOR) (...) -> (...)", line) for line in connections.split("\n")]
    values = [(x.group(1), x.group(2)) for x in values]
    connections = [(x.group(1), x.group(2), x.group(3), x.group(4)) for x in connections]
    values = {a: int(b) for a, b in values}
    connections = {d: (b, a, c) for a, b, c, d in connections}
    return values, connections


def solve1(values, connections):
    evaluated = dict(values)
    ops = {'AND': lambda a, b: a and b, 'OR': lambda a, b: a or b, 'XOR': lambda a, b: a ^ b}
    def evaluate(var):
        if var not in evaluated:
            if var in connections:
                op, a, b = connections[var]
                evaluated[var] = ops[op](evaluate(a), evaluate(b))
                #print(f"Evaluated {var} = {a} {op} {b} -> {evaluated[a]} {op} {evaluated[b]} -> {evaluated[var]}")
            else:
                raise ValueError(f"Unknown var {var}")
        return evaluated[var]
    #print(evaluated)
    for x in connections.keys():
        evaluate(x)
    z = sorted((a, int(b)) for a, b in evaluated.items() if a[0] == 'z')
    #print(z)
    #print("".join(str(b) for a,b in z), 2)
    return int("".join(str(b) for a,b in z)[::-1], 2)

def adder(n):
    #return {
    #$    f'z{i:02}': ('XOR', f"o{i:02}", f"x{i:02}", f"y{i:02}")
    #    f'o{i:02}': ('OR', )
    #}
    pass

def solve2(values, connections):
    connections = swapping(connections)
    evaluated = {}
    ops = {'AND': lambda a, b: a and b, 'OR': lambda a, b: a or b, 'XOR': lambda a, b: a ^ b}

    def evaluate(var):
        if var not in evaluated:
            if var in connections:
                op, a, b = connections[var]
                a1,b1 = sorted([evaluate(a), evaluate(b)])
                evaluated[var] = f"({a1} {op} {b1})"

                # Special case: x00 AND y00 -> car00
                if op == 'AND' and a[1:] == b[1:] == '00':
                    evaluated[var] = f"car{a1[1:]}"
                # Special case: x00 XOR y00 -> out00
                elif op == 'XOR' and a[1:] == b[1:] == '00':
                    evaluated[var] = f"out{a1[1:]}"

                # xN AND yN -> andN
                elif op == 'AND' and a[1:] == b[1:]:
                    evaluated[var] = f"and{a1[1:]}"
                # xN XOR yN -> andN
                elif op == 'XOR' and a[1:] == b[1:]:
                    evaluated[var] = f"xor{a1[1:]}"

                # carN AND xor(N+1) -> cxa(N+1)
                elif op == 'AND' and b1[:3] == 'xor' and a1[:3] == 'car' and int(a1[3:]) + 1 == int(b1[3:]):
                    evaluated[var] = f"cxa{b1[3:]}"
                # andN OR cxaN -> carN
                elif op == 'OR' and a1[:3] == 'and' and b1[:3] == 'cxa' and int(a1[3:]) == int(b1[3:]):
                    evaluated[var] = f"car{a1[3:]}"
                # carN XOR xor(N+1) -> out(N+1)
                elif op == 'XOR' and a1[:3] == 'car' and b1[:3] == 'xor' and int(a1[3:]) + 1 == int(b1[3:]):
                    evaluated[var] = f"out{b1[3:]}"
            else:
                evaluated[var] = var
        return evaluated[var]
    for x in connections.keys():
        evaluate(x)
    reverse = {b:a for a,b in evaluated.items()}
    z = sorted((a, b) for a, b in evaluated.items() if a[0] == 'z')
    for a,b in z:
        b_target = f"out{a[1:]}"
        if b != b_target:
            print(f"Found discrepancy: {a}: {b} should be {b_target}")
            print(f"Need to swap {a} and {reverse[b_target]}")
            return solve2(values, swap(connections, a, reverse[b_target]))
        print(f"{a}: {b}, {connections[a] if a in connections else ''}")
    return ",".join(sorted(['thm', 'z08', 'wrm', 'wss', 'hwq', 'z22', 'gbs', 'z29']))

def find_diff(target, actual):
    match (target, actual):
        case ((op1, a1, b1), (op2, a2, b2)) if op1 == op2:
            if a1 == a2 and b1 != b2:
                return b1, b2
            elif a1 != a2 and b1 == b2:
                return a1, a2

def expand(target):
    match target:
        case ('_OUT', 0):
            return ('XOR', ('x', 0), ('y', 0))
        #case ('_OUT', n) if n == maxN + 1:
        #    return ('OR', ('_CARRYFORTH', maxN), ('_CARRYNEW', maxN))
        case ('_OUT', n):
            return ('XOR', ('_CARRY', n-1), ('_XOR', n))

def swap(connections, a, b):
    connections = dict(connections)
    connections[a], connections[b] = connections[b], connections[a]
    return connections

def make_tree(maxN, connections):
    tree = {}

    def identify(var):
        if var not in tree:
            if var in connections:
                op, a, b = connections[var]
                a1,b1 = sorted([identify(a), identify(b)])
                tree[var] = (op, a1, b1)

                match tree[var]:
                    case ('AND', ('x', 0), ('y', 0)):
                        tree[var] = ('_CARRY', 0)
                    case ('XOR', ('x', 0), ('y', 0)):
                        tree[var] = ('_OUT', 0)
                    case ('AND', ('x', n1), ('y', n2)) if n1 == n2:
                        tree[var] = ('_CARRYNEW', n1)
                    case ('XOR', ('x', n1), ('y', n2)) if n1 == n2:
                        tree[var] = ('_XOR', n1)
                    case ('XOR', ('_CARRY', n1), ('_XOR', n2)) if n1 + 1 == n2:
                        tree[var] = ('_OUT', n2)
                    case ('AND', ('_CARRY', n1), ('_XOR', n2)) if n1 + 1 == n2:
                        tree[var] = ('_CARRYFORTH', n2)
                    case ('OR', ('_CARRYFORTH', n1), ('_CARRYNEW', n2)) if n1 == n2 == maxN:
                        tree[var] = ('_OUT', maxN + 1)
                    case ('OR', ('_CARRYFORTH', n1), ('_CARRYNEW', n2)) if n1 == n2:
                        print(f"Found the carry bit {n1} out of {maxN}")
                        tree[var] = ('_CARRY', n1)
            else:
                # base variable
                tree[var] = (var[:1], int(var[1:]))
        return tree[var]

    for x in connections.keys():
        identify(x)
        return tree

def solve3(values, connections, swaps = None):
    swaps = swaps or set()
    maxN = len(values) // 2 - 1
    tree = make_tree(maxN, connections)

    reverse = {b:a for a,b in tree.items()}
    z = sorted((a, b) for a, b in tree.items() if a[0] == 'z')
    for a,b in z:
        b_target = ('_OUT', int(a[1:]))
        if b != b_target:
            print(f"Found discrepancy: {a}: {b} should be {b_target}")
            if b_target in reverse:
                print(f"Target {b_target} found on {reverse[b_target]}...")
                print(f"Swapping wires {a} and {reverse[b_target]}")
                return solve3(values, swap(connections, a, reverse[b_target]), swaps | {a, reverse[b_target]})
            else:
                print(f"No wire found matching {b_target}")
                b_expand = expand(b_target)
                print(f"Expanding target {b_target} to {b_expand}")
                a, b = find_diff(b, b_expand)
                print(f"Diffed {a} and {b}")
                if a in reverse and b in reverse:
                    print(f"Swapping wires {reverse[a]} and {reverse[b]}")
                    return solve3(values, swap(connections, reverse[a], reverse[b]), swaps | {reverse[a], reverse[b]})
                else:
                    print("Stuck")
    else:
        print("No discrepancies, adder is clean.")
    return ",".join(sorted(swaps))

def adder(n):
    connections = {}
    names = {}
    def generate_name(name):
        if name not in names:
            number = (7 ** len(names)) & 0xfffff * int(name, 36) & 0xfffff
            names[name] = "".join(map(chr, ((97 + (number // 26**i % 26)) for i in range(3))))
        return names[name]

    connections[f'z00'] = ('XOR', 'x00', 'y00')
    connections[f'car00'] = ('AND', 'x00', 'y00')
    for i in range(1, n):
        connections[f'z{i:02}'] = ('XOR', generate_name(f"xor{i:02}"), generate_name(f"car{i-1:02}"))
        connections[generate_name(f'xor{i:02}')] = ('XOR', f"x{i:02}", f"y{i:02}")
        connections[generate_name(f'cxn{i:02}')] = ('AND', f"x{i:02}", f"y{i:02}")
        connections[generate_name(f'cxf{i:02}')] = ('AND', generate_name(f"car{i-1:02}"), generate_name(f"xor{i:02}"))
        connections[generate_name(f'car{i:02}')] = ('OR', generate_name(f"cxf{i:02}"), generate_name(f"cxn{i:02}"))
    connections[f'z{n:02}'] = connections[generate_name(f'car{n-1:02}')]
    del connections[generate_name(f'car{n-1:02}')]
    return solve3([None]*(2*(n+1)), mess_up(connections))
    #print(connections)
    return connections

def mess_up(connections):
    keys = sorted(connections.keys())
    for i in range(8):
        a = keys[(73 ** (i + 2)) % len(keys)]
        b = keys[(29 ** (i + 2)) % len(keys)]
        print(f"Swapping {a} and {b}")
        connections[a], connections[b] =connections[b], connections[a]
    return connections

def swapping(connections):
    return connections
    connections['thm'], connections['z08'] = connections['z08'], connections['thm']
    connections['wrm'], connections['wss'] = connections['wss'], connections['wrm']
    connections['hwq'], connections['z22'] = connections['z22'], connections['hwq']
    connections['gbs'], connections['z29'] = connections['z29'], connections['gbs']

    pass#connections[]

def main():
    problem = read()
    print(f"Problem 1: {solve1(*problem)}")
    print(f"Problem 2: {solve3(*problem)}")


#main()
print(adder(44))