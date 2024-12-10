import sys
from re import findall, split
from functools import reduce


def read():
	return sys.stdin.read()
    

def solve1(text):   
    return sum(int(a)*int(b) for a, b in findall(r'mul\((\d+),(\d+)\)', text))
        

def solve2(text):
    result = 0
    do = True
    for chunk in split(r"(do|don't)\(\)", text):
        if chunk == 'do':
            do = True
        elif chunk == "don't":
            do = False
        elif do:
            result += solve1(chunk)
    return result
    
def solve2b(text):
    r".*?(mul\(\d+,\d+\).*?

def main():
    text = read()
    print(f"Problem 1: {solve1(text)}")
    print(f"Problem 2: {solve2(text)}")

def debug():
    return None
    

main()
#debug()