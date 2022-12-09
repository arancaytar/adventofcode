import sys
import re
solution = None

def s1(line):
    pass


def solve1(data):
    lines = data.split("\n")
    matrix = [list(map(int, line)) for line in lines]
    width = len(matrix[0])
    height = len(matrix)
    matrix_vis = [[False]*width for i in range(height)]
    for x in range(width):
        tallest = matrix[0][x]
        matrix_vis[0][x] = True
        for y in range(1, height):
            if matrix[y][x] > tallest:
                matrix_vis[y][x] = True
                tallest = matrix[y][x]

        tallest = matrix[height-1][x]
        matrix_vis[height-1][x] = True
        for y in range(height-1, -1, -1):
            if matrix[y][x] > tallest:
                matrix_vis[y][x] = True
                tallest = matrix[y][x]

    for y in range(height):
        tallest = matrix[y][0]
        matrix_vis[y][0] = True
        for x in range(1, width):
            if matrix[y][x] > tallest:
                matrix_vis[y][x] = True
                tallest = matrix[y][x]

        tallest = matrix[y][width-1]
        matrix_vis[y][width-1] = True
        for x in range(width-1, -1, -1):
            if matrix[y][x] > tallest:
                matrix_vis[y][x] = True
                tallest = matrix[y][x]

    return sum(sum(row) for row in matrix_vis)

def s2(line):
    pass

def solve2(data):
    lines = data.split("\n")
    matrix = [list(map(int, line)) for line in lines]

    width = len(matrix[0])
    height = len(matrix)

    solution = max(scenic_score(matrix, x, y) for y in range(height) for x in range(width))
    return solution

def scenic_score(matrix, x, y):
    width = len(matrix[0])
    height = len(matrix)
    score = [0,0,0,0]
    tallest = matrix[y][x]
    for x2 in range(x+1, width):
        score[0] += 1
        if matrix[y][x2] >= tallest:
            break

    for x2 in range(x-1, -1, -1):
        score[1] += 1
        if matrix[y][x2] >= tallest:
            break

    for y2 in range(y+1, height):
        score[2] += 1
        if matrix[y2][x] >= tallest:
            break

    for y2 in range(y-1, -1, -1):
        score[3] += 1
        if matrix[y2][x] >= tallest:
            break

    #print((x, y), score)
    return score[0] * score[1] * score[2] * score[3]


#print(read_move('move 1 from 2 to 3'))
data = sys.stdin.read().strip()

#print(solve1(data))
print(solve2(data))