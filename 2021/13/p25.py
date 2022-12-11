import sys


def read():
    points, folds = sys.stdin.read().split("\n\n")
    points = list(map(lambda s: tuple(map(int, s.split(","))), points.split("\n")))
    folds = [s.split()[-1].split("=") for s in folds.split("\n")]
    folds = [(a, int(b)) for a, b in folds]
    return points, folds


def solve(points, folds):
    axis, location = folds[0]
    coord = {'x': 0, 'y': 1}[axis]
    points = set(points)
    overlaps = 0
    #print(f"Folding along {axis} = {location}")
    for point in points:
        #print(f"Processing {point}")
        point = list(point)
        if point[coord] > location:
            point[coord] = 2*location - point[coord]
            #print(f"          Becomes {point}")
            #if tuple(point) in points:
            #    print(f"                  Overlaps!")
            overlaps += tuple(point) in points
    #print(f"{overlaps} of {len(points)} points overlap")
    return len(points) - overlaps

print(solve(*read()))
