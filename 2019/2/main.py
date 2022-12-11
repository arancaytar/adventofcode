import sys

def intcode(program):
    i = 0
    while i < len(program):
        a, b, c, d = program[i:i+4]
        if a == 1:
            program[d] = program[b] + program[c]
            i += 4
        elif a == 2:
            program[d] = program[b] * program[c]
            i += 4
        elif a == 99:
            return program
        else:
            raise ValueError("Invalid op")
        #print(program)
    raise ValueError("End of file")

def run_program(program, a, b):
    program = list(program)
    program[1] = a
    program[2] = b
    return intcode(program)[0]

def search(program, output):
    for a in range(1, 100):
        for b in range(1, 100):
            try:
                if output == run_program(program, a, b):
                    return a * 100 + b
            except:
                pass

def read():
    return list(map(int, sys.stdin.read().replace(" ", "").split(",")))

print(search(read(), 19690720))