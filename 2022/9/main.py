import sys
import re
solution = None

def s1(line):
    pass

def solve1(data):
    lines = data.split("\n")
    visited = {(0,0)}
    head = tail = (0,0)
    for line in lines:
        d,s = line.split()
        s = int(s)
        for i in range(s):
            head = move_head(head, d)
            tail = move_tail(head, tail)
            visited.add(tail)
    return len(visited)


def move_head(head, direction):
    x,y = head
    if direction == 'U':
        y -= 1
    elif direction == 'R':
        x += 1
    elif direction == 'L':
        x -= 1
    elif direction == 'D':
        y += 1
    return x,y

def move_tail(head, tail):
    x1,y1 = head
    x2,y2 = tail
    dx = x1 - x2
    dy = y1 - y2
    adx = abs(dx)
    ady = abs(dy)
    sdx = dx//adx if adx else 0
    sdy = dy//ady if ady else 0
    if sdx*sdy == 0:
        if adx == 2:
            x2 += sdx
        elif ady == 2:
            y2 += sdy
    elif adx > 1 or ady > 1:
        x2 += sdx
        y2 += sdy
    return x2, y2


def s2(line):
    pass

def solve2(data):
    lines = data.split("\n")
    visited = {(0,0)}
    snake = [(0,0)]*10
    for line in lines:
        d,s = line.split()
        s = int(s)
        for i in range(s):
            snake[0] = move_head(snake[0], d)
            for j in range(1,10):
                snake[j] = move_tail(snake[j-1], snake[j])
            visited.add(snake[9])
    return len(visited)

#print(read_move('move 1 from 2 to 3'))
data = sys.stdin.read().strip()

print(solve1(data))
print(solve2(data))