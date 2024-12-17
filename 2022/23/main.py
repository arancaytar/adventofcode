import numpy as np
import sys
import collections
def read_matrix(data):
    matrix = np.array([[x == '#' for x in line] for line in data.split("\n")])
    h,w = matrix.shape
    positions = {(x,y) for x in range(w) for y in range(h) if matrix[y,x]}
    return positions

def solve1(data):
    positions = read_matrix(data)
    final, rounds = simulate(positions, 10)
    (x1,y1),(x2,y2) = boundingbox(final)
    if len(final) != len(positions):
        raise ValueError("Ant population changed?!")
    draw(final)
    return (x2-x1+1)*(y2-y1+1) - len(positions)

def solve2(data):
    positions = read_matrix(data)
    final, rounds = simulate(positions)
    (x1,y1),(x2,y2) = boundingbox(final)
    if len(final) != len(positions):
        raise ValueError("Ant population changed?!")
    draw(final)
    #return (x2-x1+1)*(y2-y1+1) - len(positions)
    return rounds

def draw(positions):
    (x1, y1), (x2, y2) = boundingbox(positions)
    matrix = np.zeros(((y2-y1+1),(x2-x1+1)),dtype=int)
    for x,y in positions:
        matrix[y-y1,x-x1] = 1
    print("\n".join(''.join('.#'[matrix[y,x]] for x in range(matrix.shape[1])) for y in range(matrix.shape[0])))

def simulate(positions, limit=10000):
    stability = 0
    priorities = ((0, -1), (0, 1), (-1, 0), (1, 0))

    i = 0
    while stability < 4 and i < limit:
        #print(len(positions))
        #draw(positions)
        positions, stable = step(positions, priorities)
        # state is stable once it has not changed for four iterations.
        # the step function can shortcut this by setting stability to four i
        stability = (stability + stable) * int(not not stable)
        #print('S', priorities)
        priorities = priorities[1:] + priorities[:1]
        #print('S done', priorities)
        i += 1
    return positions, i

def neighbor8(x, y):
    for x2 in (x-1, x, x+1):
        for y2 in (y-1, y, y+1):
            if (x2, y2) != (x, y):
                yield x2, y2


def neighbor3(x,y,dx,dy):
    if dx == 0:
        y += dy
        return {(x-1, y), (x, y), (x+1, y)}
    elif dy == 0:
        x += dx
        return {(x, y - 1), (x, y), (x, y + 1)}
    else:
        raise ValueError(f"{dx} and {dy} must not both be non-zero.")

def boundingbox(positions):
    return (
               (min(x for x,y in positions), min(y for x,y in positions)),
               (max(x for x,y in positions), max(y for x,y in positions))
    )
def step(positions, priorities):
    proposed = collections.defaultdict(set)
    moving = set()
    new_positions = set()
    for x, y in positions:
        if set(neighbor8(x, y)) & positions:
            moving.add((x, y))
        else:
            new_positions.add((x, y))
    #print('Moving', moving)
    #print('Not moving', new_positions)
    for x, y in moving:
        for dx, dy in priorities:
            if not set(neighbor3(x, y, dx, dy)) & positions:
                proposed[x+dx, y+dy].add((x,y))
                break
        else:
            new_positions.add((x, y)) # not moving after all.
    stability = 1 if proposed else 4
    for claim, claimants in proposed.items():
        if len(claimants) > 1:
            new_positions |= claimants
        else:
            new_positions.add(claim)
            stability = 0
    return new_positions, stability


data = sys.stdin.read().strip()

#print(solve1(data))
print(solve2(data))