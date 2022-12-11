import functools

matrix = []

from functools import reduce
from operator import mul

while True:
    try:
        line = input()
        matrix.append(list(map(int, line)))
    except EOFError:
        break
#print(matrix)

basins = [[None]*len(row) for row in matrix]
basin_size = {}

neighbors = (-1, 0), (1, 0), (0, -1), (0, 1)
def find_basin(matrix, i, j):
    if basins[i][j] is None:
        if matrix[i][j] == 9:
            return None
        for di, dj in neighbors:
            i2, j2 = i + di, j + dj
            if 0 <= i2 < len(matrix) and 0 <= j2 < len(matrix[i]) and matrix[i2][j2] < matrix[i][j]:
                basins[i][j] = find_basin(matrix, i2, j2)
                basin_size[basins[i][j]] += 1
                return basins[i][j]
        basins[i][j] = i,j
        basin_size[(i,j)] = 1
    return basins[i][j]

for i,row in enumerate(matrix):
    for j,height in enumerate(row):
        find_basin(matrix, i, j)

prod = lambda z : reduce(mul, z, 1)

print(prod(sorted(basin_size.values(), reverse=True)[:3]))

