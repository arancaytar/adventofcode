import sys

batteries = [list(map(int, x)) for x in sys.stdin.read().strip().split()]

def solve2(batteries, k):
    return sum(dp(bank, k) for bank in batteries)

def dp(numbers, k):
    M = [0]*k
    for x in numbers:
        M = [max(M[0], x)] + [max(M[i], M[i-1] * 10 + x) for i in range(1, k)]
    return M[k-1]

print(solve2(batteries, 2))
print(solve2(batteries, 12))