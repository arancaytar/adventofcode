import sys
from re import findall, split
from functools import reduce


def read():
	return sys.stdin.read().split()

def transpose(matrix):
    width = len(matrix[0])
    return ["".join(row[j] for row in matrix) for j in range(width)]

def diagonals(matrix):
    height, width = len(matrix), len(matrix[0])
    return ["".join(matrix[i][i+offset] for i in range(max(0, -offset), min(height, width-offset))) for offset in range(-height, width)]

def solve1(matrix):
    return (
        sum(row.count("XMAS") + row.count("SAMX") for row in matrix) # horizontal
        + sum(row.count("XMAS") + row.count("SAMX") for row in transpose(matrix)) # vertical
        + sum(diag.count("XMAS") + diag.count("SAMX") for diag in diagonals(matrix)) # diagonal
        + sum(diag.count("XMAS") + diag.count("SAMX") for diag in diagonals(matrix[::-1])) # other diagonal
    )
        

def solve2(matrix):
    height, width = len(matrix), len(matrix[0])
    count = 0
    for i in range(1, height-1):
        for j in range(1, width-1):
            found = (
                (matrix[i][j] == 'A') and 
                (
                    #({matrix[i][j-1], matrix[i][j+1]} == {matrix[i-1][j], matrix[i+1][j]} == {'S', 'M'}) + 
                    ({matrix[i-1][j-1], matrix[i+1][j+1]} == {matrix[i-1][j+1], matrix[i+1][j-1]} == {'S', 'M'})
                )
            )
            count += found
            if found:
                #print(matrix[i][j])
                #print("\n".join(matrix[i+r][j-1:j+2] for r in range(-1,2)))
                #print("---")
                #row = matrix[i][j-1:j+2]
                #col = "".join(matrix[i+r][j] for r in range(-1,2))
                diag1 = "".join(matrix[i+r][j+r] for r in range(-1,2))
                diag2 = "".join(matrix[i+r][j-r] for r in range(-1,2))
                #if row in ("SAM", "MAS") and col in ("SAM", "MAS"):
                    #print(i, j, 'reg', row, col)
#                    found -= 1
                if diag1 in ("SAM", "MAS") and diag2 in ("SAM", "MAS"):
                    print(i, j, 'diag', diag1, diag2)
                    found -= 1
                if found != 0:
                    raise ValueError("\n".join(matrix[i+r][j-1:j+2] for r in range(-1,2)))
    return count
    
def main():
    matrix = read()
    print(f"Problem 1: {solve1(matrix)}")
    print(f"Problem 2: {solve2(matrix)}")

def debug():
    return None
    

main()
#debug()