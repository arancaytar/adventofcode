import sys
from collections import Counter

def read():
	numbers = list(map(int, sys.stdin.read().split()))
	left = numbers[::2]
	right = numbers[1::2]
	return left,right
	
def solve1(left, right):
    return sum(abs(x - y) for x,y in zip(sorted(left), sorted(right)))

def solve2(left, right):
    right = Counter(right)
    return sum(x*right[x] for x in left)

def main():
    left, right = read()
    print(f"Problem 1: {solve1(left, right)}")
    print(f"Problem 2: {solve2(left, right)}")

main()