import sys
import math
import numpy as np
#import sympy as sp
#import heapq
#from collections import Counter
#from collections import deque
import re
#from fractions import Fraction
#from functools import reduce
#from operator import mul
from graph import bellman_ford_moore, DGraph, dijkstra
from grid import Grid


def read():
    #grid = Grid(sys.stdin.read())
    regs, program = sys.stdin.read().strip().split("\n\n")
    regs = [re.match(r"Register (.): (\d+)", line).groups() for line in regs.split("\n")]
    p, program = program.split()
    program = list(map(int, program.split(",")))
    return {x:int(y) for x,y in regs}, program

def machine(regs, program):
    def combo_operand(c):
        assert c < 7        
        if c > 3:
            c = regs["ABC"[c-4]]
        return c

    instruction = 0
    while instruction < len(program) - 1:
        op, operand = program[instruction:instruction+2]
        #print(f"Running {op, operand}")
        instruction += 2
        match(op):
            case 0: # ADV
                #print(f"ADV {regs['A']} >> {combo_operand(operand)} -> A")
                regs['A'] >>= combo_operand(operand)
            case 1: # BXL
                #print("BXL")
                regs['B'] ^= operand
            case 2: # BST
                #print(f"BST {combo_operand(operand)} -> B")
                regs['B'] = combo_operand(operand) & 7
            case 3: # JNZ
                #print("JNZ")
                if regs['A']:
                    instruction = operand
            case 4: # BXC
                #print(f"BXC {regs['B']} ^ {regs['C']} -> B")
                regs['B'] ^= regs['C']
            case 5: # OUT
                #print(f"OUT {combo_operand(operand)}")
                yield combo_operand(operand) & 7
            case 6: # BDV
                #print("BDV")
                regs['B'] = regs['A'] >> combo_operand(operand)
            case 7: # CDV
                #print(f"CDV {regs['A']} >> {combo_operand(operand)} -> C")
                regs['C'] = regs['A'] >> combo_operand(operand)            

class Unknown:
    def __init__(self, x):
        self.x = x
    
    def __xor__(self, other):
        if other == 0:
            return self
        return Xor(self, other)

    def __rshift__(self, other):
        return Rshift(self, other)
    
    def __repr__(self):
        return self.x
        
    def __mod__(self, n):
        assert n == 8 # always 8
        return Mod8(self)

    def resolve_bit(self, i, b):
        raise ValueError(f"Trying to resolve bit #{i} of {type(self)} instance {self} as {b}")

class Variable(Unknown):
    def __init__(self, name: str):
        self.name = name
        
    def resolve_bit(self, i, b):
        return Constraint(i, b)

    def resolve_zero(self):
        solutions = Anything()
        for i in range(64):
            solutions &= self.a.resolve_bit(i, 0)
        return solutions
        
    def resolve_nonzero(self):
        solutions = Nothing()
        for i in range(64):
            solutions += self.a.resolve_bit(i, 1)
        return solutions

    def __repr__(self):
        return self.name

class Mod8(Unknown):
    def __init__(self, a):
        self.a = a

    def __repr__(self):
        return f"({self.a} mod 8)"    

    def resolve_bit(self, i, b):
        if i > 2:
            return Anything() # don't care
        print(f"Resolving bit #{i} of {self} as {b}")
        return self.a.resolve_bit(i, b)

    def resolve(self, n):
        if not 0 <= n < 8:
            return Nothing()
        solutions = Anything()
        for i in range(3):
            solutions &= self.a.resolve_bit(i, n & 1)
            i += 1
            n >>= 1
        return solutions

    def range(self):
        return range(8)

class Xor(Unknown):
    def __init__(self, a, b):
        self.a = a
        self.b = b
        
    def __repr__(self):
        return f"({self.a} ^ {self.b})"
        
    def __xor__(self, other):
        print(f"[[[calculating {self} ^ {other}]]]")
        if type(self.a) is int and type(other) is int:
            return self.b ^ (self.a ^ other)
        if type(self.b) is int and type(other) is int:
            return self.a ^ (self.b ^ other)
        if type(self.a) is int and type(self.b) is int:
            return other ^ (self.a ^ self.b)

        return Xor(self, other)

    def range(self):
        if type(self.a) is int and type(self.b) is int:
            return [self.a ^ self.b]
        
        elif type(self.a) is int:
            yield from (b ^ self.a for b in self.b.range())

        elif type(self.b) is int:
            yield from (a ^ self.b for a in self.a.range())

        else:
            yield from {(a ^ b for a in self.a.range() for b in self.b.range())}

    def resolve(self, value):
        if type(self.a) is int and type(self.b) is int:
            return Anything() if (self.a ^ self.b) >> i == b else Nothing()
            
        if type(self.a) is int:
            return self.b.resolve(value ^ self.a)
        
        if type(self.b) is int:
            return self.a.resolve(value ^ self.b)

    def resolve_bit(self, i, b):
        print(f"Resolving bit #{i} of {self.a} ^ {self.b} as {b}")
        
        if type(self.a) is int and type(self.b) is int:
            return Anything() if (self.a ^ self.b) >> i == b else Nothing()
            
        if type(self.a) is int:
            return self.b.resolve_bit(i, (self.a >> i) & 1 ^ b)
        if type(self.b) is int:
            return self.a.resolve_bit(i, ((self.b >> i) & 1) ^ b)
            

        return (self.a.resolve_bit(i, 0) & self.b.resolve_bit(i, 1)) | (self.a.resolve_bit(i, 1) & self.b.resolve_bit(i, 0))

class Rshift(Unknown):
    def __init__(self, a, b):
        self.a = a
        self.b = b 
    
    def __repr__(self):
        return f"({self.a} >> {self.b})"

    def resolve_zero(self):
        print(f"Resolving {self.a} >> {self.b} = 0")
        if type(self.a) is int and type(self.b) is int:
            return Nothing() if (self.a >> self.b) else Anything()
        
        
        if type(self.b) is int:
            solutions = Anything()
            for i in range(self.b, self.b + 32):
                solutions &= self.a.resolve_bit(i, 0)
        
            return solutions

        solutions = Nothing()
        for b in self.b.range():
            solution = self.b.resolve(b)
            for i in range(b, b + 32):
                solutions &= self.a.resolve_bit(i, 0)
            solutions |= solution
        return solutions

    def resolve_nonzero(self):
        print(f"Resolving {self.a} >> {self.b} > 0")
        if type(self.a) is int and type(self.b) is int:
            return Anything() if (self.a >> self.b) else Nothing()
        
        if type(self.b) is int:
            solutions = Nothing()
            for i in range(self.b, self.b + 32):
                solutions |= self.a.resolve_bit(i, 0)
        
            return solutions

        solutions = Nothing()
        for b in self.b.range():
            bb = self.b.resolve(b)
            solution = Anything()
            for i in range(b, b + 32):
                solutions |= bb & self.a.resolve_bit(i, 0)
            solutions &= solution
        return solutions
        

    def resolve_bit(self, i, b):
        print(f"Resolving bit #{i} of ({self.a} >> {self.b}) to {b}")
        if type(self.b) is int:
            return self.a.resolve_bit(i + self.b, b)
        solutions = Nothing()
        for value in sorted(self.b.range()):
            print(f"... For {self.b} == {value}, resolving bit #{i + value} as {b}")
            solutions |= self.b.resolve(value) & self.a.resolve_bit(i + value, b)
        print(f"Resolved: {solutions}")
        return solutions
  
class SolutionSpace:
    pass
    
    def __add__(self, other):
        return self | other
    
class Anything(SolutionSpace):
    def __and__(self, other):
        return other
        
    def __repr__(self):
        return "ALL"

class Nothing(SolutionSpace):
    def __and__(self, other):
        return Nothing()
    
    def __or__(self, other):
        return other

    def __repr__(self):
        return "∅"

    def expand(self):
        return []

class Constraint(SolutionSpace):
    def __init__(self, *args):
        if type(args[0]) is set:
            self.constraint_sets = args[0]
            self.reduce()
            assert self.constraint_sets, f"Empty constraint set created. Did you mean Nothing()?"
        else:
            i, b = args
            self.constraint_sets = {frozenset({(i, b)})}

    def reduce(self):
        reduced_const = set()
        removing = False
        for const in self.constraint_sets:
            for bit, value in const:
                relax = const - {(bit, value)}
                alt = relax | {(bit, 1-value)}
                if relax in self.constraint_sets:
                    removing = True
                    break
                if alt in self.constraint_sets:
                    reduced_const.add(relax)
                    removing = True
                    break
            else:
                reduced_const.add(const)
        self.constraint_sets = reduced_const
        if removing:
            self.reduce()

    def __repr__(self):
        def repr(constraints):
            x = dict(constraints)
            return "".join(str(x[i]) if i in x else "-" for i in range(1+max(x.keys())))[::-1]# + str(x)

        return "|".join(sorted(repr(constraints) for constraints in self.constraint_sets))

    def __len__(self):
        return len(self.constraint_sets)
        
    def __and__(self, other):
        if type(other) is Anything:
            return self
        if type(other) is Nothing:
            return other

        assert type(other) is Constraint, f"Trying to combine with {other}."

        print(f"Combining constraint sets of size {len(self.constraint_sets)} x {len(other.constraint_sets)}")
        new_const = set()
        for constraints1 in self.constraint_sets:
            for constraints2 in other.constraint_sets:
                contradiction = False
                combo = {}
                for bit, value in constraints1:
                    combo[bit] = value
                for bit, value in constraints2:
                    if bit in combo and combo[bit] != value:
                        contradiction = True
                        break
                    combo[bit] = value
                    
                if contradiction:
                    continue

                new_const.add(frozenset(combo.items()))
        if new_const:
            x = Constraint(new_const)
        else:
            x = Nothing()
        print(f"Combined set is {x}")
        return x

    def expand(self):
        for const in self.constraint_sets:
            x = dict(const)
            cc = "".join(str(x[i]) if i in x else "-" for i in range(1+max(x.keys())))[::-1]
            print(f"Expanding constraint {cc}")
            skeleton = sum(1<<i for (i, b) in const if b)
            print(skeleton)
            print(bin(skeleton))
            open = sorted(set(range(1 + max(x.keys()))) - x.keys())
            def recurse(a, x):
                if x >= 0:
                    yield from recurse(a, x - 1)
                    yield from recurse(a + 1<<open[x], x - 1)
                else:
                    yield a
                    
            yield from recurse(skeleton, len(open) - 1) 
            

    def __or__(self, other):
        if type(other) is Anything:
            return Anything
        if type(other) is Nothing:
            return self
        
        return Constraint(self.constraint_sets | other.constraint_sets)

def reverse_machine(regs, program, output, instruction=0, visited_states=frozenset()):
    print(f"Starting program with {regs}, pointer at {instruction}, testing for {output}")
    visited = set(visited_states)
    def combo_operand(c):
        assert c < 7        
        if c > 3:
            c = regs["ABC"[c-4]]
        return c
    
    def rshift(a, b):
        if type(a) is Unknown or type(b) is int:
            return a >> b
        if a == 0:
            return 0
        return Rshift(a, b)
    
    def xor(a, b):
        if type(a) is Unknown or type(b) is int:
            return a ^ b
        if a == 0:
            return b
        if b == 0:
            return a
        return Xor(a, b)

    regs['A'] = Variable("a")
    output_index = 0
    
    solution_space = Anything()
    
    while instruction < len(program) - 1:
        state = (f"{regs['A'], regs['B'], regs['C']}", instruction)
        if state in visited:
            print(f"Revisited {state} in {len(visited)}, halting this branch.")
            return Nothing() # forbid loops
        visited.add(state)

        op, operand = program[instruction:instruction+2]
        print(f"Running #{instruction}: {op, operand}")
        instruction += 2
        match(op):
            case 0: # ADV
                print(f"ADV {regs['A']} >> {combo_operand(operand)} -> A       ((={rshift(regs['A'], combo_operand(operand))}))")
                regs['A'] = rshift(regs['A'], combo_operand(operand))
            case 1: # BXL
                print(f"BXL {regs['B']} ^ {operand} -> B     (={xor(regs['B'], operand)})")
                regs['B'] = xor(regs['B'], operand)
            case 2: # BST
                print(f"BST {combo_operand(operand)} -> B")
                regs['B'] = combo_operand(operand) % 8
            case 3: # JNZ
                print("JNZ")
                # Jump or don't jump:
                packaged = frozenset(visited)
                print("Testing no-jump")
                option1 = regs['A'].resolve_zero() & reverse_machine(dict(regs), program, output[output_index:], instruction, packaged) 
                print("Testing jump")
                option2 = regs['A'].resolve_nonzero() & reverse_machine(dict(regs), program, output[output_index:], operand, packaged)
                print(f"Combining {solution_space} & ({option1} | {option2})...")
                return solution_space & (option1 | option2)
            case 4: # BXC
                print(f"BXC {regs['B']} ^ {regs['C']} -> C     (={xor(regs['B'], regs['C'])})")
                regs['B'] = xor(regs['B'], regs['C'])
            case 5: # OUT
                print(f"OUT #{output_index}: {combo_operand(operand)}")
                if output_index >= len(output):
                    return Nothing()
                print(f"Must output {output[output_index]}, outputting {combo_operand(operand) % 8}")
                #if output_index == 0:
                #    print(f"First output guaranteed by A & 7 == 6")
                #else:
                #    assert output[output_index] == combo_operand(operand) % 8
                solution_space = solution_space & Mod8(combo_operand(operand)).resolve(output[output_index])
                output_index += 1
            case 6: # BDV
                print("BDV")
                regs['B'] = rshift(regs['A'], combo_operand(operand))
            case 7: # CDV
                print(f"CDV {regs['A']} >> {combo_operand(operand)} -> C")
                regs['C'] = rshift(regs['A'], combo_operand(operand))

    return solution_space
    
def solve1(regs, program):
    return ",".join(map(str, machine(regs, program)))


def solve2(regs, program):
#    regs['A'] = 6
#    print(program, solve1(regs, program))
    print("Starting search")
    constraints = reverse_machine(regs, program, program)
    print("Finished search")
    print(f"Solutions are <{constraints}>")
    for i, n in enumerate(constraints.expand()):
        print(n)
        print(bin(n))
        regs['A'] = n
        output = list(machine(dict(regs), program))
        if output == program:
            return n
        print(output)
        if i > 10:
            break
    #for constraint in constraints

def solve2_bruteforce(regs, program):
    for i in range(6, 10**8, 8):
        regs2 = dict(regs)
        regs2['A'] = i
        output = list(machine(regs2, program))
        #print(i, bin(i), program, output)
        if program == output:
            return i

def main():
    problem = read()
    #print(f"Problem 1: {solve1(*problem)}")
    print(f"Problem 2: {solve2(*problem)}")
    #print(f"Problem 2: {solve2_bruteforce(*problem)}")

def debug():
    return None
    

main()
#debug()



 