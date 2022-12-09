def read_lines():
    while True:
        try:
            yield input()
        except EOFError:
            break

def mapper():
    mapper_ = {c:i-4 for i,c in enumerate('<{[( )]}>')}
    return lambda c: mapper_[c]

def score(char):
    return [0, 3, 57, 1197, 25137][char]

def check_syntax(mapper):
    def _(line):
        stack = None

        for char in map(mapper, line):
            if char < 0:
                stack = (char, stack)
            else:
                open, stack = stack
                if char != -open:
                    return score(char)
        if stack:
            # incomplete
            pass
        return 0
    return _

def main():
    return sum(map(check_syntax(mapper()), read_lines()))

print(main())