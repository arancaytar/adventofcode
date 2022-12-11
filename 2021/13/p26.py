import functools
import sys


def read():
    points, folds = sys.stdin.read().split("\n\n")
    points = list(map(lambda s: tuple(map(int, s.split(","))), points.split("\n")))
    folds = [s.split()[-1].split("=") for s in folds.split("\n")]
    folds = [(a, int(b)) for a, b in folds]
    return points, folds


def run_fold(points, axis, location):
    coord = {'x': 0, 'y': 1}[axis]
    points = set(points)
    new_points = set()
    for point in points:
        point = list(point)
        if point[coord] > location:
            point[coord] = 2*location - point[coord]
        new_points.add(tuple(point))
    return new_points

def solve(points, folds):
    for axis, location in folds:
        points = run_fold(points, axis, location)
    return points

def output(points):
    w, h = map(lambda d: functools.reduce(max, d), zip(*points))
    matrix = [[' ']*(w+1) for i in range(h+1)]
    for x,y in points:
        matrix[y][x] = '#'
    print(*("".join(row) for row in matrix), sep="\n")

data = read()
p = solve(*data)
#output(data[0])
output(p)
