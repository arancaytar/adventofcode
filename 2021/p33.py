def solve(x1, x2, y1, y2):
    time = 0
    for i in range(x1):
        if i * (i + 1) // 2 > x2:
            time = i - 1
            break
    print(time)

def velocities(dx, dy):
    while True:
        yield dx, dy
        dx = dx - (dx > 0) + (dx < 0)
        dy -= 1

def positions(x, y, dx1, dy1):
    for dx, dy in velocities(dx1, dy1):
        x += dx
        y += dy
        #print(x, y)
        yield x, y


def simulate(dx1, dy1, x1, x2, y1, y2):
    maxheight = 0
    for x, y, in positions(0, 0, dx1, dy1):
        maxheight = max(maxheight, y)
        if x1 <= x <= x2 and y1 <= y <= y2:
            return maxheight
        if x > x2 or y < y1:
            return 0

def brute(x1, x2, y1, y2):
    mh = 0
    for i in range(max(abs(x1), abs(x2))):
        for j in range(max(abs(y1), abs(y2))):
            mh = max(mh, simulate(i, j, x1, x2, y1, y2))
    return mh
#print(brute(20, 30, -10, -5))
print(brute(119, 176, -141,-84))
