import numpy as np
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
        filter(None, re.split(r'(R|L)', path))
    ]
    return board, path

def simulate1(board, path):
    x,y,d = 0,0,0
    draw = np.array(board)
    yield (x,y,d), draw
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
            forward, backward = steps[d], steps[(d + 2) % 4]
            for i in range(instruction):
                #print(f"  #{i}", x, y)

                # Try to walk forward.
                x2, y2 = forward(x, y)
                #print("   ",x2, y2)
                #print(bound_check(x2, y2), bound_check(x2, y2) and (board[y2, x2] != 2))

                # Check if we would go out of bounds.
                if not bound_check(x2, y2) or board[y2,x2] == 2:
                    # If so, go back from our current position until we go out of bounds on the opposite side.
                    x2, y2 = x, y
                    #print("Wrapping back from ", x2, y2, d)
                    while bound_check(x2, y2) and board[y2,x2] != 2:
                        x2, y2 = backward(x2, y2)
                    # Go one step forward to be back inside bounds.
                    x2, y2 = forward(x2, y2)
                # Check if we would hit rock (possibly after wrapping around)
                if board[y2,x2] == 1:
                    #print(f"Hit rock at {x2,y2}!")
                    # If so, stop moving and continue with the next instruction.
                    break
                else:
                    draw[y, x] = 3+d
                    # If we would move into an open space, confirm our new position.
                    x, y = x2, y2
                #print("     ", x, y)
            draw2 = np.array(draw)
            draw2[y,x] = 7
            yield (x, y, d), draw2
            #print("\n".join(''.join('.# >v<^X'[draw2[y, x]] for x in range(w)) for y in range(h)))
    return (y+1)*1000 + (x+1)*4 + d
