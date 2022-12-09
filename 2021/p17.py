matrix = []

while True:
    try:
        line = input()
        matrix.append(list(map(int, line)))
    except EOFError:
        break
#print(matrix)
def low_points(matrix):
    neighbors = (-1, 0), (1, 0), (0, -1), (0, 1)

    def check(i, j):
        for di, dj in neighbors:
            i2, j2 = i + di, j + dj
            if 0 <= i2 < len(matrix) and 0 <= j2 < len(matrix[i]):
                if matrix[i2][j2] <= matrix[i][j]:
                    return False
        return True

    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if check(i, j):
                yield matrix[i][j] + 1

print(sum(low_points(matrix)))