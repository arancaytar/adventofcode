import sys
import functools
import operator

def read():
    return sys.stdin.read().strip().split("\n")
def read1(lines):
    operands = [list(map(int, l.split())) for l in lines[:-1]]
    operators = lines[-1].split()
    return operands, operators

def read2(lines):
    o = lines[:-1]
    transposed = ["".join(l[i] for l in o) for i in range(len(o[0]))]
    transposed = " ".join(x if x.strip() else "\n" for x in transposed)
    operands = [list(map(int, t.strip().split())) for t in transposed.split("\n")]
    return operands, lines[-1].split()
def solve1(operands, operators):
    return sum(
        functools.reduce({'+': operator.add, '*': operator.mul}[op], (l[i] for l in operands))
        for i, op in enumerate(operators)
    )

def solve2(operands, operators):
    return sum(
        functools.reduce({'+': operator.add, '*': operator.mul}[op], l)
        for l, op in zip(operands, operators)
    )

def main():
    x = read()
    print(solve1(*read1(x)))
    print(solve2(*read2(x)))

main()