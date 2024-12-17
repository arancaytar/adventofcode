
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
        #print(f"!{count}/{len(path)}", x, y, d, f"<{instruction}>")
        if instruction == 'L':
            d = (d + 3) % 4
        elif instruction == 'R':
            d = (d + 1) % 4
        elif type(instruction) == int:
            for i in range(instruction):
                #print(f"  #{i}", x, y)

                # Try to walk forward.
                x2, y2 = steps[d](x, y)
                next_d = d
                #print("   ",x2, y2)
                #print(bound_check(x2, y2), bound_check(x2, y2) and (board[y2, x2] != 2))

                # Check if we would go out of bounds.
                if not bound_check(x2, y2) or board[y2,x2] == 2:
                    # warp to the correct position by cube rules.
                    x2, y2, next_d = warp(x,y, x2, y2, d)
                # Check if we would hit rock (possibly after wrapping around)
                if board[y2,x2] == 1:
                    #print(f"Hit rock at {x2,y2}!")
                    # If so, stop moving and continue with the next instruction.
                    break
                else:
                    draw[y, x] = 3+d
                    # If we would move into an open space, confirm our new position.
                    x, y, d = x2, y2, next_d
                #print("     ", x, y)
            draw2 = np.array(draw)
            draw2[y,x] = 7

            #print("\n".join(''.join('.# >v<^X'[draw2[y, x]] for x in range(w)) for y in range(h)))
        else:
            raise ValueError(f"Invalid instruction #{count} <{instruction}")

    print(x,y,d)
    return (y+1)*1000 + (x+1)*4 + d

def warp_sample(x, y, x2, y2, direction):
    if 8 <= x < 12 and y == 0 and x2 == x and y2 == -1 and direction == 3:
        return 11 - x, 4, 1
    elif x == 8 and 0 <= y < 4 and x2 == 7 and y2 == y and direction == 2:
        return 4 + y, 4, 1
    elif 4 <= x < 8 and y == 4 and x2 == x and y2 == 3 and direction == 3:
        return 8, x - 4, 0
    elif 0 <= x < 4 and y == 4 and x2 == x and y2 == 3 and direction == 3:
        return 11 - x, 0, 1
    elif x == 0 and 4 <= y < 8 and x2 == -1 and y2 == y and direction == 2:
        return 19 - y, 11, 3
    elif 0 <= x < 4 and y == 7 and x2 == x and y2 == 8 and direction == 1:
        return 11 - x, 11, 3
    elif 4 <= x < 8 and y == 7 and x2 == x and y2 == 8 and direction == 1:
        return 8, 15 - x, 0
    elif x == 8 and 8 <= y < 12 and x2 == 7 and y2 == y and direction == 2:
        return 15 - y, 7, 3
    elif 8 <= x < 12 and y == 11 and x2 == x and y2 == 12 and direction == 1:
        return 11 - x, 7, 3
    elif 12 <= x < 16 and y == 11 and x2 == x and y2 == 12 and direction == 1:
        return 0, 19 - x, 0
    elif x == 15 and 8 <= y < 12 and x2 == 16 and y2 == y and direction == 0:
        return 11, 11 - y, 2
    elif 12 <= x < 16 and y == 8 and x2 == x and y2 == 7 and direction == 3:
        return 11, 19 - x, 2
    elif x == 11 and 4 <= y < 8 and x2 == 12 and y2 == y and direction == 0:
        return 19 - y, 8, 1
    elif x == 11 and 0 <= y < 4 and x2 == 12 and y2 == y and direction == 0:
        return 15, 11 - y, 2
    else:
        raise ValueError(f"Fell off the edge of the map at ({x}, {y}) -> ({x2}, {y2}) (${direction}).")

def get_warper(warp_zones, size):
    warp_lookup = {}
    for a, b in warp_zones:
        warp_lookup[a] = b
        warp_lookup[b] = a

    def warp(x, y, x2, y2, d):
        face, side, index = get_edge(x, y, x2, y2, d, size)
        source = (face[0], face[1], side)
        if source not in warp_lookup:
            raise ValueError(f"Warp zone {source} is not known.")
        target = warp_lookup[source]
        # the clockwise index is always reversed when moving between adjacent faces.
        # to visualize this, picture the faces as interlocking gears - their rotations must be mirrored.
        return map_edge(target, size, size - 1 - index)

    return warp


def warp_zones_input():
    warp_zones = {
        ((1, 0, 'top'), (0, 3, 'left')),
        ((1, 0, 'left'), (0, 2, 'left')),
        ((1, 1, 'left'), (0, 2, 'top')),
        ((0, 3, 'bottom'), (2, 0, 'top')),
        ((0, 3, 'right'), (1, 2, 'bottom')),
        ((1, 2, 'right'), (2, 0, 'right')),
        ((1, 1, 'right'), (2, 0, 'bottom'))
    }
    return warp_zones

def get_edge(x, y, x2, y2, d, size):
    # Returns coordinates of square, type of edge, index in clockwise direction along edge.
    face = x // size, y // size
    on_face = x % size, y % size
    side, index = None, None
    if x2 == x:
        if on_face[1] == 0 and y2 == y - 1 and d == 3:
            side, index = 'top', on_face[0]
        elif on_face[1] == size - 1 and y2 == y + 1 and d == 1:
            side, index = 'bottom', size - 1 - on_face[0]
    elif y2 == y:
        if on_face[0] == 0 and x2 == x - 1 and d == 2:
            side, index = 'left', size - 1 - on_face[1]
        elif on_face[0] == size - 1 and x2 == x + 1 and d == 0:
            side, index = 'right', on_face[1]
    if side and index is not None:
        return face, side, index
    else:
        raise ValueError(f"Fell off the edge of the map at ({x}, {y}) -> ({x2}, {y2}) (${d}) on face {face}/{on_face}.")

def map_edge(target, size, index):
    fx, fy, side = target
    fx, fy = fx * size, fy * size
    if side == 'top':
        return fx + index, fy, 1
    elif side == 'right':
        return fx + size - 1, fy + index, 2
    elif side == 'bottom':
        return fx + size - 1 - index, fy + size - 1, 3
    elif side == 'left':
        return fx, fy + size - 1 - index, 0
    else:
        raise ValueError(f"Unknown side {side}.")

def solve1(data):
    board, path = read_input(data)

    #return
    return simulate1(board, path)

warp = get_warper(warp_zones_input(), 50)

data = sys.stdin.read()
print(solve1(data))
