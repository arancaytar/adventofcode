import sys
import numpy as np
import re
import collections
import ortools

def solve1(data):
    lines = data.split("\n")
    sensors = []
    y_line = 2000000
    #y_line = 10
    ranges = []
    excluded_count = 0
    beacons_y = set()
    for line in lines:
        m = re.match('Sensor at x=([-\d]+), y=([-\d]+): closest beacon is at x=([-\d]+), y=([-\d]+)', line)
        x,y,x2,y2 = map(int, (m.group(i) for i in range(1, 5)))
        if y2 == y_line:
            beacons_y.add(x2)
        dist = abs(y - y_line)
        size = abs(x2 - x) + abs(y2 - y)
        if dist > size:
            continue
        x_start = x - (size - dist)
        x_end = x + (size - dist)
        #print(x,y, x_start, x_end, x_end - x_start + 1)
        ranges.append((x_start, x_end))
    ranges = sorted(ranges)
    #print(ranges)
    excluded_count -= len(beacons_y)
    open_end = ranges[0][1]
    excluded_count += ranges[0][1] - ranges[0][0] + 1
    for x_start, x_end in ranges[1:]:
        #print(excluded_count, open_end, x_start, x_end)
        if x_start > open_end:
            # disjoint
            open_end = x_end
            excluded_count += x_end - x_start + 1
            continue
        elif x_end <= open_end:
            # contained
            continue
        else:
            excluded_count += x_end - open_end
            open_end = x_end

    return excluded_count




    print(sensors)

def solve2(data):
    lines = data.split("\n")
    sensors = []
    ranges = []
    excluded_count = 0


    for line in lines:
        m = re.match('Sensor at x=([-\d]+), y=([-\d]+): closest beacon is at x=([-\d]+), y=([-\d]+)', line)
        x,y,x2,y2 = map(int, (m.group(i) for i in range(1, 5)))
        size = abs(x2-x) + abs(y2-y)
        sensors.append((x,y,size))
        print(rf"abs(x-{x}) + abs(y-{y}) < {size}")

    for i in range(len(sensors)):
        for j in range(i+1, len(sensors)):
            intersect = intersect_diamonds(sensors[i], sensors[j])


def intersect_diamonds(s1, s2):
    if s1[2] < s2[2]:
        s1,s2 = s2,s1
    x1,y1,d1 = s1
    x2, y2, d2 = s2
    # constraint1: abs(x3-x1) + abs(y3-y1) == d1 + 1
    # constraint2: abs(x3-x2) + abs(y3-y2) == d2 + 1

data = sys.stdin.read().strip()

print(solve1(data))
print(solve2(data))