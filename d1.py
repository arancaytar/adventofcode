import sys

def a1(numbers: list):
    numbers.sort()
    # for each number, look for the complement to 2020.
    for x in numbers:
        y = 2020 - x
        if binsearch(numbers, y) is not None:
            return x * y
        # don't bother giving up after 1010, since we are promised a solution.

def a2(numbers: list):
    numbers.sort()
    # for each pair of numbers
    for i,x in enumerate(numbers):
        for y in numbers[i+1:]:
            z = 2020 - x - y
            # x < y < z
            if z <= y:
                break
            if binsearch(numbers, z) is not None:
                return x * y * z


def binsearch(z, k):
    a, b = 0, len(z) - 1
    while a < b:
        c = (a + b) // 2
        if z[c] < k:
            a = c+1
        elif z[c] > k:
            b = c-1
        else:
            return c
    if z[a] == k:
        return a
    return None


print(a2(list(map(int, sys.stdin.read().split()))))