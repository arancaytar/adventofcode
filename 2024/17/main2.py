import sys
import re

def read():
    #grid = Grid(sys.stdin.read())
    regs, program = sys.stdin.read().strip().split("\n\n")
    regs = [re.match(r"Register (.): (\d+)", line).groups() for line in regs.split("\n")]
    p, program = program.split()
    program = list(map(int, program.split(",")))
    return {x:int(y) for x,y in regs}, program

def machine(regs, program):
    oo = lambda n: oct(n)[2:]
    def combo_operand(c):
        assert c < 7        
        if c > 3:
            c = regs["ABC"[c-4]]
        return c

    def repreg(regs):
        return f"<{oo(regs['A'])}>\t<{oo(regs['B'])}>\t<{oo(regs['C'])}>"

    instruction = 0
    while instruction < len(program) - 1:
        op, operand = program[instruction:instruction+2]
        #print(f"#{instruction}: {op}{operand} -\t\t\t REG {repreg(regs)}")
        instruction += 2
        match(op):
            case 0: # ADV
                #print(f"ADV {oo(regs['A'])} >> {combo_operand(operand)} -> A")
                regs['A'] >>= combo_operand(operand)
            case 1: # BXL
                #print(f"BXL {oo(regs['B'])} ^ {operand} -> B")
                regs['B'] ^= operand
            case 2: # BST
                #print(f"BST {oo(combo_operand(operand))} & 7 -> B")
                regs['B'] = combo_operand(operand) & 7
            case 3: # JNZ
                #print(f"JNZ {operand}? {regs['A'] > 0}")
                if regs['A']:
                    instruction = operand
            case 4: # BXC
                #print(f"BXC {oo(regs['B'])} ^ {oo(regs['C'])} -> B")
                regs['B'] ^= regs['C']
            case 5: # OUT
                #print(f"OUT {oo(combo_operand(operand))} & 7")
                #print(f"<<<<<< {combo_operand(operand) & 7}")
                yield combo_operand(operand) & 7
            case 6: # BDV
                #print(f"BDV {regs['A']} >> {combo_operand(operand)} -> B")
                regs['B'] = regs['A'] >> combo_operand(operand)
            case 7: # CDV
                #print(f"CDV {regs['A']} >> {combo_operand(operand)} -> C")
                regs['C'] = regs['A'] >> combo_operand(operand)            

def next_octal(prefix, target_digit):
    for i in range(8):        
        output = list(machine({'A': prefix << 3 | i, 'B': 0, 'C': 0}, (2,4,1,1,7,5,1,5,4,5,0,3,5,5,3,0)))
        if output and output[0] == target_digit:
            yield i

def solve1(regs, program):
    #print(regs['A'])
    #print(regs['A'] ^ 1)
    return ",".join(map(str, machine(regs, program)))

def solve2(regs, program):
    n = regs['A']
    regs['A'] = 0o310
    return ",".join(map(str, machine(regs, program)))

def solve3():
    def run(a):
        return list(machine({'A': 4, 'B': 0, 'C': 0}, program))
    program = [2,4,1,1,7,5,1,5,4,5,0,3,5,5,3,0]
    output = []
    prefix = 0
    while len(output) < len(program):
        d = list(next_octal(prefix, program[-1-len(output)]))
        print(f"Found solutions: {d}")
        assert len(d) == 1, f"No definite solution for this digit."
        [d] = d
        output = run(d)
        print(f"Next digit is {d}: {output}")
        prefix = prefix << 3 | d
        #print(f"Last digit is {next_octal(0, output[-1])}")

def next_octal(prefix, target_digit):
    for i in range(8):        
        output = list(machine({'A': prefix << 3 | i, 'B': 0, 'C': 0}, (2,4,1,1,7,5,1,5,4,5,0,3,5,5,3,0)))
        if output and output[0] == target_digit:
            yield i

def solve4():
    a = '  '
    def recurse(prefix, target):
        depth = 0 if not prefix else len(oct(prefix)) - 2
        indent = a * depth
        print(f"{indent}Find next octal to append to {oct(prefix)[2:]} to yield final digit of {target}")
        if not target:
            print(f"We're done here, returning {prefix} as only solution.")
            return [prefix]
        solutions = []
        for d in next_octal(prefix, target[-1]):
            print(f"{indent}Found digit {d}: {run(prefix << 3 | d)}")
            solutions += recurse(prefix << 3 | d, target[:-1])
        print(f"Emerging with {solutions}")
        return solutions
    def run(a):
        return list(machine({'A': a, 'B': 0, 'C': 0}, program))
    program = [2,4,1,1,7,5,1,5,4,5,0,3,5,5,3,0]
    return min(recurse(0, program))

def main():
    problem = read()
    #print(f"Problem 1: {solve1(*problem)}")
    #print(f"Problem 1: {solve2(*problem)}")
    print(f"Problem 2: {solve4()}")
    

    
    
main()