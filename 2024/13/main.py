import sys
import math
import numpy as np
import sympy as sp
import heapq
from collections import Counter
from collections import deque
import re
from fractions import Fraction

def read():
    prizes = sys.stdin.read().strip().split("\n\n")
    return [list(map(int, re.match(r"Button A: X.(\d+), Y.(\d+)\nButton B: X.(\d+), Y.(\d+)\nPrize: X=(\d+), Y=(\d+)", prize).groups())) for prize in prizes]


def sample():
    m = np.matrix([[94, 34],[22,67]])
    xy = np.array([8400, 5400])
    ab = np.array([80, 40])
    print(xy * m**-1)
    
def sample2(): 
    available = []
    ax, ay, bx, by, x, y = 5, 5, 1, 1, 17, 17
    print(ax, ay, bx, by, x, y)
    m = sp.Matrix([[ax, ay],[bx,by]])
    xy = sp.Matrix([[x, y]])
    print("     ", xy)
    try:
        a, b = xy * (m**-1)
        print("     ",a, b)
        if a.denominator == b.denominator == 1:
            available.append(int(3 * a) + int(b))
    except sp.matrices.exceptions.NonInvertibleMatrixError:
        a1,a2 = sp.Rational(x, ax), sp.Rational(y, ay)
        b1,b2 = sp.Rational(x, bx), sp.Rational(y, by)
        if a1 == a2 and b1 == b2:
            if x % max(ax,bx) % min(ax,bx) == 0:
                if ax < 3*bx: # prefer B
                    remainder = x % bx
                    b = x // bx
                    a = 0
                    while remainder % ax and remainder <= x:
                        remainder += bx
                        b -= 1
                    if remainder % ax == 0:
                        a = remainder // ax
                        available.append(3*a + b)
                elif ax >= 3*bx: # prefer A
                    remainder = x % ax
                    a = x // ax
                    b = 0
                    while remainder % bx and remainder <= x:
                        remainder += ax
                        a -= 1
                    if remainder % bx == 0:
                        b = remainder // bx
                        available.append(3*a + b)
    print(a, b)

def solve1(*prizes):
    #a, b = sp.Symbol('A'), sp.Symbol('B')
    available = []
    for ax,ay,bx,by,x,y in prizes:
        #print(ax, ay, bx, by, x, y)
        m = sp.Matrix([[ax, ay],[bx,by]])
        xy = sp.Matrix([[x, y]])
        #print("     ", xy)
        try:
            a, b = xy * (m**-1)
            #print("     ",a, b)
            if a.denominator == b.denominator == 1:
                    available.append(int(3 * a) + int(b))
        except sp.matrices.exceptions.NonInvertibleMatrixError:
            a1,a2 = sp.Rational(x, ax), sp.Rational(y, ay)
            b1,b2 = sp.Rational(x, bx), sp.Rational(y, by)
            if a1 == a2 and b1 == b2:
                if x % max(ax,bx) % min(ax,bx) == 0:
                    if ax < 3*bx: # prefer B
                        remainder = x % bx
                        b = x // bx
                        a = 0
                        while remainder % ax and remainder <= x:
                            remainder += bx
                            b -= 1
                        if remainder % ax == 0:
                            a = remainder // ax
                            available.append(3*a + b)
                    elif ax >= 3*bx: # prefer A
                        remainder = x % ax
                        a = x // ax
                        b = 0
                        while remainder % bx and remainder <= x:
                            remainder += ax
                            a -= 1
                        if remainder % bx == 0:
                            b = remainder // bx
                            available.append(3*a + b)
    return sum(available)
  
    
def solve2(*prizes):
    return solve1(*[(ax, bx, ay, by, x + 10000000000000, y + 10000000000000) for ax, bx, ay, by, x, y in prizes])
    
def main():
    problem = read()
    #print(f"S: {sample2()}")
    print(f"Problem 1: {solve1(*problem)}")
    print(f"Problem 2: {solve2(*problem)}")
    #print(f"Problem 1+2: {solve(*problem)}")

def debug():
    return None
    

main()
#debug()



 