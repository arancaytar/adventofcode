import sys
import re
import numpy as np
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

def simulate1(board, path):
    x,y,d = 0,0,0
    draw = np.array(board)
    h,w = board.shape
    while board[y,x]:
        x += 1
        if x >= w:
            x = 0
            y += 1
    #print('start', x,y)
    steps = [
        lambda x, y: (x + 1, y),
        lambda x, y: (x, y + 1),
        lambda x, y: (x - 1, y),
        lambda x, y: (x, y - 1),
    ]
    bound_check = lambda x3, y3: 0 <= x3 < w and 0 <= y3 < h
    for count, instruction in enumerate(path):
        print(f"!{count}/{len(path)}", x, y, d, f"<{instruction}>")
        if instruction == 'L':
            d = (d + 3) % 4
        elif instruction == 'R':
            d = (d + 1) % 4
        elif type(instruction) == int:
            forward, backward = steps[d], steps[(d + 2) % 4]
            for i in range(instruction):
                print(f"  #{i}", x, y)

                # Try to walk forward.
                x2, y2 = forward(x, y)
                #print("   ",x2, y2)
                #print(bound_check(x2, y2), bound_check(x2, y2) and (board[y2, x2] != 2))

                # Check if we would go out of bounds.
                if not bound_check(x2, y2) or board[y2,x2] == 2:
                    # If so, go back from our current position until we go out of bounds on the opposite side.
                    x2, y2 = x, y
                    print("Wrapping back from ", x2, y2, d)
                    while bound_check(x2, y2) and board[y2,x2] != 2:
                        x2, y2 = backward(x2, y2)
                    # Go one step forward to be back inside bounds.
                    x2, y2 = forward(x2, y2)
                # Check if we would hit rock (possibly after wrapping around)
                if board[y2,x2] == 1:
                    print(f"Hit rock at {x2,y2}!")
                    # If so, stop moving and continue with the next instruction.
                    break
                else:
                    draw[y, x] = 3+d
                    # If we would move into an open space, confirm our new position.
                    x, y = x2, y2
                print("     ", x, y)
            draw2 = np.array(draw)
            draw2[y,x] = 7
        else:
            raise ValueError(f"Invalid instruction #{count} <{instruction}")
            #print("\n".join(''.join('.# >v<^X'[draw2[y, x]] for x in range(w)) for y in range(h)))
    print(x,y,d)
    return (y+1)*1000 + (x+1)*4 + d

def solve1(data):
    board, path = read_input(data)

    #return
    return simulate1(board, path)

def cube(board):
    non_zeros = np.sum(board != 2)
    h, w = board.shape
    n = int((non_zeros // 6)**0.5)
    faces = [[board[y:y+n,x:x+n] for x in range(0, w, n)] for y in range(0, h, n)]
    faces_mask = np.array([[int(np.any(face != 2)) for face in row] for row in faces])
    fh, fw = faces_mask.shape

    neighbors_index = [[None]*fw for i in range(fh)]

    for y in range(fh):
        for x in range(fw):
            if faces_mask[y,x]:
                neighbors_index[y][x] = [None] * 4
                for i, (x2,y2) in enumerate(((x+1, y), (x,y+1), (x-1, y), (x,y-1))):
                    if 0 <= x2 < fw and 0 <= y2 < fh and faces_mask[y2,x2]:
                        neighbors_index[y][x][i] = (x2, y2, (i + 2) % 4)
    print(neighbors_index)
    return


    faces_index = [(-10,-10)]*6

    faces_reverse_index = np.zeros((fh, fw)) - 1
    def find_first_nonempty():
        for y in range(fh):
            for x in range(fw):
                if faces_mask[y, x]:
                    return x, y
    t1 = find_first_nonempty()
    faces_index[0] = t1
    faces_reverse_index[t1] = 0
    def neighbors(x, y):
        return [
            (x2, y2) for x2, y2 in ((x-1, y), (x,y-1), (x+1,y), (x,y+1)) if 0 <= x2 < fw and 0 <= y2 <= fh and faces_mask[y2,x2]
        ]
    t2 = neighbors(*t1)[0]
    faces_index[1] = t2
    faces_reverse_index[t2] = 1
    print(faces_index, faces_reverse_index)

class CrazyCube:
    def __init__(self, faces, size):
        self.faces = faces
        self.size = size
        self.face, self.x, self.y, self.heading = 't', 0, 0, 0

    def rotate(self, direction):
        if direction == 'L':
            self.heading = (self.heading + 3) % 4
        elif direction == 'R':
            self.heading = (self.heading + 1) % 4
        else:
            raise ValueError("Invalid direction for turning.")
    def move(self):
        if self.heading == 0:
            x, y = self.x + 1, self.y
        elif self.heading == 1:
            x, y = self.x, self.y + 1
        elif self.heading == 2:
            x, y = self.x - 1, self.y
        elif self.heading == 3:
            x, y = self.x, self.y - 1
        else:
            raise ValueError("Invalid heading.")

        return self.try_move(self.face, x, y)

    def try_move(self, face, x, y):
        if x < 0:
            if face == 't': # off the top to the left (west)
                target = ('w', self.y, 0, 1)
            elif face == 'b': # off the bottom to the left (east)
                target = ('e', self.size - 1 - self.y, self.size - 1, 3)
            else: # CCW around the cube
                target = ({'w': 'n', 'n': 'e', 'e': 's', 's': 'w'}[face], self.size - 1, self.y, 2)
        elif x >= self.size:
            if face == 't':
                target = ('e', self.size - 1 - self.y, 0, 1)
            elif face == 'b':
                target = ('w', self.y, self.size - 1, 3)
            else:
                target = ({'n': 'w', 'w': 's', 's': 'e', 'e': 'n'}[face], 0, self.y, 0)
        elif y < 0:
            if face == 't':
                target = ('n', self.size - 1 - x, 0, 1)
            elif face == 'b':
                target = ('n', self.x, self.size - 1, 3)
            elif face == 'n':
                target = ('t', self.size - 1 - self.x, 0, 1)
            elif face == 'e':
                target = ('t', self.size - 1, self.size - 1 - self.x, 2)
            elif face == 's':
                target = ('t', self.x, self.size - 1, 3)
            elif face == 'w':
                target = ('t', 0, self.x, 0)
        elif y >= self.size:
            if face == 't':
                target = ('s', self.x, 0, 1)
            elif face == 'b':
                target = ('s', self.size - 1 - self.x, self.size - 1, 3)
            elif face == 'n':
                target = ('b', self.x, 0, 1)
            elif face == 'e':
                target = ('b', 0, self.x, 0)
            elif face == 's':
                target = ('b', self.size - 1 - self.x, self.size - 1, 3)
            elif face == 'w':
                target = ('b', self.size - 1, self.size - 1 - x, 2)
        else:
            target = (self.face, x, y, self.heading)

        if self.faces[target[0]][target[2],target[1]]:
            return False
        else:
            self.face, self.x, self.y, self.heading = target
            return True

def read_sample_cube(board):
    faces = {}
    faces['t'] = board[0:4, 8:12]
    faces['s'] = board[4:8, 8:12]
    faces['w'] = board[4:8, 4:8]
    faces['n'] = board[4:8, 0:4]
    faces['b'] = np.rot90(np.rot90(board[8:12, 8:12]))
    faces['e'] = np.rot90(board[8:12, 12:16])
    return CrazyCube(faces, 4)

#def read_input_cube(board):
#    faces = {}
#    faces['t'] = board[0:50, 50:100]
#    faces['e'] = np.rot90(board[0:50, 100:150])
#    faces['w'] = board[4:8, 4:8]
#    faces['n'] = board[4:8, 0:4]
#    faces['b'] = np.rot90(np.rot90(board[8:12, 8:12]))
#    faces['e'] = np.rot90(board[8:12, 12:16])

def solve2_cube(c: CrazyCube, path):
    for instruction in path:
        if type(instruction) == str:
            c.rotate(instruction)
        else:
            for i in range(instruction):
                if not c.move():
                    break
    return

data = sys.stdin.read()
#print(solve1(data))
board, path = read_input(data)
#print(cube(board))

c = read_sample_cube(board)
