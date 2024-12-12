import sys
import math
import numpy as np
import heapq
from collections import Counter

def read():
    return (list(map(int, sys.stdin.read().strip().split())),)

def l(number):
    return int(math.log10(number)) + 1

def solve1(numbers):
    #print(numbers)
    for i in range(25):
        numbers2 = []
        for number in numbers:
            if number == 0:
                numbers2.append(1)
            else:
                le = l(number)
         #       print(le)
                if le % 2 == 0:
                    d = 10 ** (le // 2)
                    numbers2 += [number // d, number % d]
                else:
                    numbers2.append(number * 2024)
        numbers = numbers2
        #print(numbers)
    return len(numbers)

def solve2(numbers):
    numbers = Counter(numbers)
    for i in range(75):
        numbers2 = Counter()
        for number, pop in numbers.items():
            if number == 0:
                numbers2[1] += pop
            else:
                le = l(number)
         #       print(le)
                if le % 2 == 0:
                    d = 10 ** (le // 2)
                    numbers2[number // d] += pop
                    numbers2[number % d] += pop
                else:
                    numbers2[number * 2024] += pop
        numbers = numbers2
        #print(numbers)
    return sum(numbers.values())

def step(numbers: Counter) -> Counter:
    numbers2 = Counter()
    for number, pop in numbers.items():
        if number == 0:
            numbers2[1] += pop
        else:
            le = l(number)
            if le % 2 == 0:
                d = 10 ** (le // 2)
                numbers2[number // d] += pop
                numbers2[number % d] += pop
            else:
                numbers2[number * 2024] += pop
    return numbers2

def solve(numbers, steps):
    numbers = Counter(numbers)
    for i in range(steps):
        numbers = step(numbers)
    print(len(numbers), numbers.most_common(10))
    return sum(numbers.values())
    
def solve1(numbers):
    return solve(numbers, 25)

def solve2(numbers):
    return solve(numbers, 75)

    
def main():
    problem = read()
    print(f"Problem 1: {solve1(*problem)}")
    print(f"Problem 2: {solve2(*problem)}")

def debug():
    return None
    

main()
#debug()