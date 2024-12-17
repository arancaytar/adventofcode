import numpy as np
import sys
import re
def read_input(data):
    board, path = data.split("\n\n")
    board = board.split("\n")
    #print(board)
    width = max(len(row) for row in board)
    board = [row + ' '*(width - len(row)) for row in board]
    #print(board)
    board = np.array([[{'.':0,'#':1,' ':2}[x] for x in line] for line in board])
    path = [
        int(x) if x.isdigit() else x
        for x in
        filter(None, re.split(r'(R|L)', path.strip()))
    ]
    return board, path

def cube(board):
    non_zeros = np.sum(board != 2)
    h, w = board.shape
    n = int((non_zeros // 6)**0.5)
    faces = [[board[y:y+n,x:x+n] for x in range(0, w, n)] for y in range(0, h, n)]
    faces_mask = np.array([[int(np.any(face != 2)) for face in row] for row in faces])
    print(faces_mask)
    fh, fw = faces_mask.shape

    def find_first_nonempty():
        for y in range(fh):
            for x in range(fw):
                if faces_mask[y, x]:
                    return x, y
    top_face = find_first_nonempty()

    def neighbors(x, y):
        return {
            i:((x2, y2) if 0 <= x2 < fw and 0 <= y2 <= fh and faces_mask[y2,x2] else None) for i,(x2, y2) in enumerate(((x+1, y), (x,y+1), (x-1,y), (x,y-1)))
        }
    print(top_face)
    top_neighbors = neighbors(*top_face)
    if top_neighbors[0]:
        east_face = top_neighbors[0]
        east_face_top_edge = 2
    if top_neighbors[1]:
        south_face = top_neighbors[1]
        south_face_top_edge = 3
    if top_neighbors[2]:
        west_face = top_neighbors[2]
        west_face_top_edge = 0
    if top_neighbors[3]:
        north_face = top_neighbors[3]
        north_face_top_edge = 1

    print(top_neighbors)

data = sys.stdin.read()
#print(solve1(data))
board, path = read_input(data)
print(cube(board))