import sys
import re
solution = None

def s1(line):
    pass

def solve1(data):
    diag, moves = data.split("\n\n")
    matrix = parse_diagram(diag)
    for move in moves.split("\n"):
        matrix = apply_move(matrix, read_move(move))
    return "".join(r[-1] for r in matrix)

def s2(line):
    pass

def solve2(data):
    lines = data.split()
    return sum(map(s2, lines))

    return solution


def parse_diagram(data):
    lines = data.split("\n")

    stack_number = (max(map(len, lines))+1)//4
    matrix = [[] for i in range(stack_number)]
    for line in lines:
        line = line + " "*(4*stack_number)
        for i in range(stack_number):
            print(i)
            char = line[4*i + 1]
            if char != ' ':
                matrix[i].append(char)
    matrix = [s[::-1] for s in matrix]
    return matrix

def read_move(line):
    group = re.match('move (\d+) from (\d+) to (\d+)', line)
    return tuple(map(int, group.groups()))

def apply_move(matrix, move):
    count, start, end = move
    boxes = matrix[start-1][-count:]
    matrix[start-1] = matrix[start-1][:-count]
    matrix[end-1] += boxes
    return matrix



#print(read_move('move 1 from 2 to 3'))
data = sys.stdin.read()

print(solve1(data))
#print(solve2(data))