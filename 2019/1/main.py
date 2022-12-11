import sys

def a1(numbers):
    return sum(sum(fuel_rec(n))-n for n in numbers)

def fuel(n):
    return n//3 - 2

def fuel_rec(n):
    while n > 0:
        #print(n)
        yield n
        n = n // 3 - 2

print(a1(map(int, sys.stdin.read().split())))