import sys

batteries = [list(map(int, x)) for x in sys.stdin.read().strip().split()]
def solve1(batteries):
    n, m = len(batteries), len(batteries[0])
    maxright = [[0]*m for i in range(n)]
    for i,bank in enumerate(batteries):
        maxright[i][-1] = bank[-1]
        for j in range(2, m):
            maxright[i][-j] = max(maxright[i][1-j], bank[-j])

    total = 0
    for i,bank in enumerate(batteries):
        optimum = 0
        #print(bank, maxright[i])
        for j in range(m-1):
            optimum = max(optimum, bank[j] * 10 + maxright[i][j+1])
        #print(optimum)
        total += optimum
    return total

def solve2(batteries):
    total = 0
    for bank in batteries:
        optimum = dp(bank, 12)
        print(optimum)
        total += optimum
    return total


def dp(numbers, k):
    n = len(numbers)
    M = [0]*k
    for x in numbers:
        M_new = [0]*k
        M_new[0] = max(M[0], x)
        for i in range(1, k):
            M_new[i] = max(M[i], M[i-1] * 10 + x)
        M = M_new
    return M[k-1]


print(solve2(batteries))