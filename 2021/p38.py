import numpy as np
import sys
def primitive_turns():
    return [
        np.matrix([[1, 0, 0], [0, 0, -1], [0, 1, 0]]), # rotate z y
        np.matrix([[0, 0, -1], [0, 1, 0], [1, 0, 0]]), # rotate z x
        np.matrix([[0, -1, 0], [1, 0, 0], [0, 0, 1]]) # rotate x y
    ]


def all_turns():
    status = {tuple(np.eye(3).flatten()): np.eye(3)}
    turns = primitive_turns()
    a, b = 0, 1
    while a < b:
        for matrix in list(status.values()):
            for turn in turns:
                m = turn * matrix
                status[hash(m)] = m
        a, b = b, len(status)
    return list(status.values())

#    (x, y, z), (-z, y, x), (-x, y, -z), (z, y, -x),
#    (-y, x, z), (-z, x, -y), (y, x, -z), (z, x, y),
#    (-x, -y, z), (-z, -y, -x), (x, -y, -z), (z, -y, x),
#    (y, -x, z), (-z, -x, y), (-y, -x, -z), (x, -x, y),

#    (x, -z, y),         (-x, z, y),
#    (-y, z, x),         (y, z, x),
#    (-x, -z, -y),        (x, z, -y),
#    (y, -z, -x),        (-y, z, -x)
#    )

def hash(v):
    return tuple(*(v.flatten().tolist()))

def count_overlaps(s1,s2):
    return set(map(hash, s1)) & set(map(hash, s2))

def apply_turn(s, turn):
    return list(map(lambda v:turn*v, s))

def apply_move(s, rel):
    return list(map(lambda v:v+rel, s))

def check_against_regularized(scanner, regularized, turns, checked, index):
    for i in regularized:
        if (i, index) not in checked:
            break
    else:
        return None,None
    for turn in turns:
        scanner_ = apply_turn(scanner, turn)
        for i,s2 in regularized.items():
            if (i, index) in checked:
                continue
            for p1 in scanner_[:-11]:  # twelve HAVE to overlap. after checking all but 11, give up.
                for p2 in s2[:-11]:
                    relative = p1 - p2
                    s2_ = apply_move(s2, relative)
                    ov = count_overlaps(scanner_, s2_)
                    if len(ov) >= 12:
                        return apply_move(scanner_, -relative), relative
    for i in regularized:
        checked.add((i, index))
        checked.add((index, i))
    return None,None


def check_scanners(scanners):
    turns = all_turns()
    regularized = {0: scanners[0]}
    positions = {0: (0,0,0)}
    checked = set()
    while len(regularized) < len(scanners):
        print(f"{len(regularized)}, {len(scanners)}")
        progress = False
        for i, scanner in enumerate(scanners):
            if i in regularized:
                continue
            print(f"Checking {i}")
            scanner_,rel = check_against_regularized(scanner, regularized, turns, checked, i)
            if scanner_:
                regularized[i] = scanner_
                positions[i] = hash(rel)
                print("Match!")
                print(max_manhattan(positions.values()))
                progress = True
        if not progress:
            print(f"Failing with {len(regularized)}")
            raise ValueError("No progress")
    #return max_manhattan(set().union(*(set(map(hash, scanner)) for scanner in regularized.values())))
    return max_manhattan(positions.values())

def max_manhattan(points):
    dist = 0
    for x1,y1,z1 in points:
        for x2,y2,z2 in points:
            dist = max(dist, abs(x1-x2)+abs(y1-y2)+abs(z1-z2))
    return dist

#for m in relative_turns():
#    print(m)
#    print(m * np.array([[1], [2], [3]]))

def read():
    text = sys.stdin.read().strip().split("\n\n")
    scanners = [x.split("\n")[1:] for x in text]
    scanners = [[np.matrix(list(map(int, l.split(",")))).transpose() for l in scanner] for scanner in scanners]
    return scanners

print(check_scanners(read()))