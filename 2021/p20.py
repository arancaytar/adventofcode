from collections import deque

def read_lines():
    while True:
        try:
            yield input()
        except EOFError:
            break

def mapper():
    mapper_ = {c:i-4 for i,c in enumerate('<{[( )]}>')}
    return lambda c: mapper_[c]

def invalid_score(char):
    return [0, 3, 57, 1197, 25137][char]

def incomplete_score(stack):
    score = 0
    while stack:
        score = 5*score - stack.pop()
    return score

def check_syntax(mapper):
    def _(line):
        stack = deque()

        for char in map(mapper, line):
            if char < 0:
                stack.append(char)
            else:
                open = stack.pop()
                if char != -open:
                    #return invalid_score(char)
                    return 0
        if stack:
            return incomplete_score(stack)
        return 0
    return _

def median(z):
    z = sorted(z)
    return z[len(z)//2]

def main():
    return median(filter(None, map(check_syntax(mapper()), read_lines())))

print(main())