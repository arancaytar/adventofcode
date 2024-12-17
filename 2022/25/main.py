import sys

def to_dec(d):
    r = 0
    for x in d:
        r = (r * 5) + x
    return r

def to_snafu(dec: int):
    digits = []
    while dec:
        digits.append((dec + 2) % 5 - 2)
        dec = (dec - digits[-1]) // 5
    return ''.join({-2: '=', -1: '-', 0: '0', 1: '1', 2: '2'}[x] for x in digits[::-1])

def read_number(s):
    return [{'=': -2, '-': -1, '0': 0, '1': 1, '2': 2}[x] for x in s]

def solve1(data):
    return to_snafu(sum(list(map(to_dec, map(read_number, data.split("\n"))))))

data = sys.stdin.read()
print(solve1(data))