from collections import deque


def read_matrix():
    matrix = []
    while True:
        try:
            matrix.append(list(map(int, input().strip())))
        except EOFError:
            break
    return matrix


def step(matrix, n, m):
    activated = set()
    activate = deque()
    for i in range(n):
        for j in range(m):
            matrix[i][j] += 1
            if matrix[i][j] > 9:
                activate.append((i, j))
                activated.add((i, j))
    while activate:
        i, j = activate.popleft()
        for di in (-1, 0, 1):
            for dj in (-1, 0, 1):
                if di or dj:
                    i2, j2 = i + di, j + dj
                    if 0 <= i2 < n and 0 <= j2 < m and (i2, j2) not in activated:
                        matrix[i2][j2] += 1
                        if matrix[i2][j2] > 9:
                            activate.append((i2, j2))
                            activated.add((i2, j2))
        for i, j in activated:
            matrix[i][j] = 0
    return len(activated)


def run(matrix, steps):
    n, m = len(matrix), len(matrix[0])
    return sum(step(matrix, n, m) for i in range(steps))

print(run(read_matrix(), 100))