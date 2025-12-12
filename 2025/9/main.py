import sys
def read():
    return [tuple(map(int, l.split(","))) for l in sys.stdin.read().strip().split()]


def solve1(coords):
    n = len(coords)
    return max(area(coords[i], coords[j]) for i in range(n) for j in range(i + 1, n))

def area(p1, p2):
    #print(p1, p2, abs((p1[0] - p2[0]) * p1[1] - p2[1]))
    return (abs(p1[0] - p2[0]) + 1) * (abs(p1[1] - p2[1]) + 1)
def solve2(coords):
    constraints = get_constraints(coords)
    n = len(coords)
    candidates = ((coords[i], coords[j]) for i in range(n) for j in range(i + 1, n) if check_constraints(coords[i], coords[j], constraints))
    best = max(candidates, key=lambda x:area(*x))
    draw(coords, best)
    return area(*best)
def draw(coords, rect):
    w = max(c[0] for c in coords)
    h = max(c[1] for c in coords)
    f = open('output.svg', 'w')
    lines = (f"L {c[0]} {c[1]}" for c in coords[1:])
    x1, x2 = sorted((rect[0][0], rect[1][0]))
    y1, y2 = sorted((rect[0][1], rect[1][1]))
    f.write(f'''
<svg width="{w}" height="{h}" xmlns="http://www.w3.org/2000/svg">
    <path d="M {coords[0][0]} {coords[0][1]} {' '.join(lines)}" />
    <rect x="{x1}" y="{y1}" width="{x2-x1}" height="{y2-y1}" fill="red" />
</svg>''')
    f.close()

def check_constraints(p1, p2, constraints):
    debug = p1 == (9, 5) and p2 == (2, 3)

    # bounding box
    x1, x2 = sorted((p1[0], p2[0]))
    y1, y2 = sorted((p1[1], p2[1]))
    if debug:
        print('BB', x1, y1, x2, y2)

    for axis, sign, c, (a, b) in constraints:
        if (axis, sign) == ('x', 1) and x1 < c < x2 and not (b <= y1 or a >= y2):
            if debug:
                print(p1, p2, axis, sign, c, (a, b))
            return False
        elif (axis, sign) == ('x', -1) and x2 > c > x1 and not (b <= y1 or a >= y2):
            if debug:
                print(p1, p2, axis, sign, c, (a, b))
            return False
        elif (axis, sign) == ('y', 1) and y1 < c < y2 and not (b <= x1 or a >= x2):
            if debug:
                print(p1, p2, axis, sign, c, (a, b))
            return False
        elif (axis, sign) == ('y', -1) and y2 > c > y1 and not (b <= x1 or a >= x2):
            if debug:
                print(p1, p2, axis, sign, c, (a, b))
            return False
    return True

def get_constraints(coords):
    n = len(coords)
    turns = 0
    directions = []
    for i in range(1, n):
        p1, p2 = coords[i-1:i+1]
        dx, dy = p2[0] - p1[0], p2[1] - p1[1]
        if dx * dy:
            raise ValueError("Consecutive points must be collinear")
        if dx > 0:
            direction = 1
        elif dx < 0:
            direction = 3
        elif dy > 0:
            direction = 2
        else:
            direction = 0
        directions.append(direction)

    current_dir = directions[0]
    for dir in directions[1:]:
        turn = ((dir - current_dir) + 2) % 4 - 2
        turns += turn
        #print(current_dir, turn, turns)
        current_dir = dir
    if abs(turns) != 4:
        raise ValueError("Broken assumption of exactly one full clockwise or counterclockwise overall turn.")

    inside_dir = 1 if turns > 0 else -1

    constraints = []
    for i, dir in enumerate(directions):
        p1, p2 = coords[i:i+2]
        if dir == 0: # vertical constraint
            constraints.append(('x', inside_dir, p1[0], sorted((p1[1], p2[1]))))
        elif dir == 1:
            constraints.append(('y', inside_dir, p1[1], sorted((p1[0], p2[0]))))
        elif dir == 2:
            constraints.append(('x', -inside_dir, p1[0], sorted((p1[1], p2[1]))))
        else:
            constraints.append(('y', -inside_dir, p1[1], sorted((p1[0], p2[0]))))
    return constraints
def main():
    coords = read()
    print(solve1(coords))
    print(solve2(coords))

main()