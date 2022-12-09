import sys
import re
solution = None

def s1(line):
    return next(i+4 for i in range(len(line)-4) if len(set(line[i:i+4])) == 4)

def solve1(data):
    #lines = data.split()
#    return sum(map(s2, lines))
    return next(i + 14 for i in range(len(data) - 14) if len(set(data[i:i + 14])) == 14)


def s2(line):
    pass

def solve2(data):
    lines = data.split()
    return sum(map(s2, lines))

    return solution



#print(read_move('move 1 from 2 to 3'))
data = sys.stdin.read()

print(solve1(data))
#print(solve2(data))