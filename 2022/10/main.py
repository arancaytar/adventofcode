import sys
import re
solution = None

def s1(line):
    pass

def simulate(lines):
    history = [1]
    for instruction in lines:
        if instruction == 'noop':
            history.append(history[-1])
        else:
            a,b = instruction.split()
            history.extend((history[-1], history[-1] + int(b)))
    return history

def solve1(data):
    lines = data.split("\n")
    history = simulate(lines)
    strength = [history[i] * (i+1) for i in range(19, len(history), 40)]
    #print(history)
    #print([(history[i], (i + 1)) for i in range(19, len(history), 40)])
    #print(strength)
    return sum(strength)

def s2(line):
    pass

def solve2(data):
    lines = data.split("\n")
    history = simulate(lines)
    print(*(
        println(history[i:i+40])
        for i in range(0, len(history), 40)
    ), sep="\n")

def println(register):
    if len(register) < 40:
        return ""
    return "".join((
       '.#'[abs(i - register[i]) <= 1] for i in range(40)
    ))

#print(read_move('move 1 from 2 to 3'))
data = sys.stdin.read().strip()

print(solve1(data))
print(solve2(data))