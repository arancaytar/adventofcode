import sys
from functools import cmp_to_key
from math import log10
from operator import add, mul
def read():
    data = sys.stdin.read().strip().split("\n")
    lines = [list(map(int, line.replace(":", "").split())) for line in data]
    return ([(line[0], line[1:]) for line in lines],)

def binary_to_vector(n, b):
    for i in range(n):
        yield b & 1
        b >>= 1

def trinary_to_vector(n, t):
    for i in range(n):
        yield t % 3
        t //= 3

def evaluate(target, operands, operators):
    result = operands[0]
    operators = list(operators)
    for operator, operand in zip(operators, operands[1:]):
        if operator:
            result *= operand
        else:
            result += operand
        if result > target:
            return False
    return result == target

def evaluate2(target, operands, operators):
    result = operands[0]
    for operator, operand in zip(operators, operands[1:]):
        if operator == 2:
            result = int(f"{result}{operand}")
        elif operator:
            result *= operand
        else:
            result += operand
        if result > target:
            return False
    return result == target

def search(result, operands):
    n = len(operands)
    for i in range(1<<(len(operands)-1)):
        if evaluate(result, operands, binary_to_vector(n, i)):
            return True
    return False

def search2(result, operands):
    n = len(operands)
    for i in range(3**(len(operands)-1)):
        if evaluate2(result, operands, trinary_to_vector(n, i)):
            return True
    return False

def solve1_slow(numbers):
    return sum(result for result, operands in numbers if search(result, operands))
    
def solve2_slow(numbers):
    return sum(result for result, operands in numbers if search2(result, operands))

def solve1(numbers):
    return sum(result for result, operands in numbers if search_rec1(result, operands))

def search_rec1(target, operands):
    n = len(operands) - 1
    def _rec(result, i):
        if i > n:
            return result == target
        if result > target:
            return False
        return _rec(result + operands[i], i+1) or _rec(result * operands[i], i+1)

    return _rec(operands[0], 1)

def solve2(numbers):
    return sum(result for result, operands in numbers if search_rec2(result, operands))

def search_rec2(target, operands):
    n = len(operands) - 1
    def _rec(result, i):
        if i > n:
            return result == target
        if result > target:
            return False
        #if int(str(result) + "".join(map(str,operands[i:]))) < target:
        #    return False
        return _rec(result + operands[i], i+1) or _rec(result * operands[i], i+1) or _rec(concat(result, operands[i]), i+1)

    return _rec(operands[0], 1)

def check_reachable(result, operands, operators):
    reachable = {operands[0]}
    for i, x in enumerate(operands[1:], 1):
        new_reachable = set()
        for y in reachable:
            for op in operators:
                if i == len(operands) - 1:
                    if op(y, x) == result:
                        return True
                    continue
                r = op(y, x)
                if r < result:
                    new_reachable.add(r)
        reachable = new_reachable
    return False


def solve2_memo(numbers):
    return sum(result for result, operands in numbers if check_reachable(result, operands, (add, mul, lambda x, y: int(str(x) + str(y)))))

def search_backward(target, operands):
    if target and not operands:
        return False
    if (target % operands[-1]) and (target % (10**int(log10(operands[-1]) + 1)) != operands[-1]):
        return search_backward(target - operands[-1], operands[:-1])
    return search_rec2(target, operands)

def solve2_backward(numbers):
    return sum(result for result, operands in numbers if search_backward(result, operands))

def solve2_both_ends(numbers):
    return sum(result for result, operands in numbers if search_both_ends(result, operands))

def concat(a, b):
    return a * 10**(int(log10(b))+1) + b

def cut(a, b):
    '''Remove b as a suffix from a. If b is not a suffix of a, return None.'''
    w = 10**(int(log10(b))+1)
    return a // w if a % w == b else None

def search_both_ends(target, operands):
    i, j = 1, len(operands) - 1
    left, right = {operands[0]}, {target}
    while i <= j:
        if len(left) < len(right):
            a = operands[i]
            left = {x + a for x in left} | {x * a for x in left} | {concat(x, a) for x in left}
            i += 1
        else:
            b = operands[j]
            right = {x - b for x in right} | {x // b for x in right if x % b == 0} | set(filter(None, (cut(x, b) for x in right)))
            j -= 1
    return len(left & right) > 0
    

# 1 + 2 * 3 = 9
# i,j,left,right = 1, 2, {1}, {9}
# i,j,left,right = 1, 1, {1}, {3 (* 3 = 9), 6 (+ 3 = 9)} = {3, 6}
# i,j,left,right = 2, 1, {(1 + 2 =) 3, (1 * 2) = 2} = {2, 3}, {3, 6}


def main():
    problem = read()
    print(f"Problem 1: {solve1(*problem)}")
    #print(f"Problem 2: {solve2(*problem)}")
    #print(f"Problem 2: {solve2_memo(*problem)}")
    #print(f"Problem 2: {solve2_backward(*problem)}")
    print(f"Problem 2: {solve2_both_ends(*problem)}")

def debug():
    return None
    

main()
#debug()