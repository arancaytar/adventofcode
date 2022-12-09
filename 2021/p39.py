import sys

def readline(s):
    return list(map(lambda x:x == '#', s.strip()))

def write_matrix(matrix):
    for row in matrix:
        print("".join('.#'[x] for x in row))

def read():
    program, matrix = sys.stdin.read().split("\n\n")
    program = readline(program)
    matrix = list(map(readline, matrix.strip().split("\n")))
    return program, matrix

def getcode(matrix, i, j, outside):
    n, m = len(matrix), len(matrix[0])
    code = 0
    for i2 in range(i - 1, i + 2):
        for j2 in range(j - 1, j + 2):
            if (0 <= i2 < n) and (0 <= j2 < m):
                code = (code << 1) + matrix[i2][j2]
            else:
                code = (code << 1) + outside
    return code

def step(program, matrix, outside):
    n, m = len(matrix), len(matrix[0])
    matrix2 = [[0]*(m+2) for i in range(n+2)]
    for i in range(-1, n+1):
        for j in range(-1, m+1):
            code = getcode(matrix, i, j, outside)
            matrix2[i+1][j+1] = program[code]
    outside = program[0]
    return matrix2, outside

def solve(program, matrix, steps=2):
    outside = 0
    for i in range(steps):
        matrix, outside = step(program, matrix, outside)
        write_matrix(matrix)
        print(outside)
        print("---")
    print(sum(sum(row) for row in matrix))

print(solve(*read()))