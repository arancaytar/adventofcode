import sys
import itertools
import functools
def read():
    return list(map(read_machine, sys.stdin.read().strip().split("\n")))

def read_machine(s):
    m = s.split()
    lights = sum((x=='#')<<i for i,x in enumerate(m[0][1:-1]))
    buttons1 = tuple(sum(1<<int(c) for c in x[1:-1].split(",")) for x in m[1:-1])
    buttons2 = tuple(tuple(map(int, x[1:-1].split(","))) for x in m[1:-1])
    voltages = tuple(map(int, m[-1][1:-1].split(",")))
    return lights, buttons1, buttons2, voltages

def xsum(z):
    return functools.reduce(lambda a, b: a ^ b, z, 0)

def solve1(machines):
    return sum(len(solve1_machine(lights, buttons)) for lights, buttons, _ _ in machines)

def solve1_machine(lights, buttons):
    for k in range(len(buttons)):
        for b in itertools.combinations(buttons, k):
            if not (xsum(b) ^ lights):
                return b
def solve2():
    return sum(len(solve1_machine(buttons, voltages)) for _, _, buttons, voltages in machines)

def solve2_machine(buttons, voltages):
    

def main():
    machines = read()
    print(solve1(machines))
    print(solve2())

main()