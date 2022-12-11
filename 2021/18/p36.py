import copy
from collections import deque
import sys

class Number:
    def __init__(self):
        self.parent = None
        self.index = None

    def set_parent(self, parent: 'Pair', index: int):
        self.parent = parent
        self.index = index

    def __add__(self, other):
        pair = Pair(self, other)
        reduce_number(pair)
        return pair

    def __radd__(self, other):
        if other == 0:
            return self

    def __int__(self):
        raise NotImplemented()

class Atom(Number):
    def __init__(self, val: int):
        super().__init__()
        self.val = val

    def set(self, val: int):
        self.val = val

    def split(self):
        self.parent.set(self.index, Pair(Atom(self.val//2), Atom((self.val+1)//2)))

    def __repr__(self):
        return f"<{self.val}>"

    def __int__(self):
        return self.val

    def __deepcopy__(self, memo:dict):
        return Atom(self.val)

class Pair(Number):
    def __init__(self, a: Number, b: Number):
        super().__init__()
        self.a = a
        a.set_parent(self, 0)
        self.b = b
        b.set_parent(self, 1)

    def set(self, index, value: Number):
        value.set_parent(self, index)
        if index == 0:
            self.a = value
        elif index == 1:
            self.b = value

    def explode(self):
        assert (isinstance(self.a, Atom))
        assert (isinstance(self.b, Atom))
        left = self.find_prev_atom()
        right = self.find_next_atom()
        #print(f"Right atom is {right}")
        if isinstance(left, Atom):
            left.set(left.val + self.a.val)
        if isinstance(right, Atom):
            right.set(right.val + self.b.val)
        assert (isinstance(self.parent, Pair))
        self.parent.set(self.index, Atom(0))

    def find_prev_atom(self):
        index = self.index
        current = self.parent
        while index == 0 and current is not None:
            index, current = current.index, current.parent
        if current is not None:
            current = current.a
        while not isinstance(current, Atom) and current is not None:
            current = current.b
        return current

    def find_next_atom(self):
        index = self.index
        current = self.parent
        #print(f"Next atom: parent is {current}")
        while index == 1 and current is not None:
            #print("Next atom: Going up")
            index, current = current.index, current.parent
        if current is not None:
            current = current.b
        while not isinstance(current, Atom) and current is not None:
            #print("Next atom: Going right")
            current = current.a
        return current

    def __repr__(self):
        return f"[{self.a},{self.b}]"

    def __int__(self):
        return 3 * int(self.a) + 2 * int(self.b)

    def __deepcopy__(self, memodict):
        return Pair(copy.deepcopy(self.a), copy.deepcopy(self.b))

def read_number(string):
    stack = deque()
    for c in string.strip():
        match c:
            case '[' | ',':
                stack.append(c)
            case ']':
                right, comma, left, open = (stack.pop() for i in range(4))
                stack.append(Pair(left, right))
            case _ if '0' <= c <= '9':
                stack.append(Atom(int(c)))
            case _:
                raise ValueError(f"Unrecognized token {c}")
    assert len(stack) == 1
    #print(stack)
    return stack[0]


def reduce_number(number: Number):
    #print(number)
    if explode_number(number):
        #print("Exploded, redo from start")
        return reduce_number(number)
    if split_number(number):
        #print("Splitted, redo from start")
        return reduce_number(number)
    #print("Done")
    return number


def explode_number(number: Number, depth=0) -> bool:
    # Only pairs explode
    if not isinstance(number, Pair):
        return False
    # Only pairs of atoms at depth 4+ explode
    if depth < 4 or not (isinstance(number.a, Atom) and isinstance(number.b, Atom)):
        return explode_number(number.a, depth+1) or explode_number(number.b, depth+1)
    number.explode()
    return True


def split_number(number: Number) -> bool:
    if isinstance(number, Atom):
        return number.val > 9 and (number.split() or True)
    if isinstance(number, Pair):
        return split_number(number.a) or split_number(number.b) or False
    return False

def read():
    return map(read_number, sys.stdin.read().strip().split("\n"))

def main():
    x = sys.stdin.read().strip().split("\n")
    print(max(int(read_number(x[i]) + read_number(x[j]))
               for i in range(len(x)) for j in range(len(x)) if i != j))


main()

#print(*map(reduce_number, read()),sep="\n")

#print(read_number('[[[[4,3],4],4],[7,[[8,4],9]]]') + read_number('[1,1]'))

#print(sum(map(read_number, ['[1,1]', '[2,2]', '[3,3]', '[4,4]'])))

