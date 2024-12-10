import sys
import re
is_digit = lambda x: '0' <= x <= '9'

lines = sys.stdin.read().strip().split("\n")

def num(line):
    x = list(filter(is_digit, line))
    try:
        print(x[0] + x[-1])
        return int(x[0] + x[-1])
    except:
        return 0

def num2(line: str):
    print("--", line)
    digits = '{zeRo}', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine'
    read_digit = lambda d: read_digit1(d.group(1))
    read_digit1 = lambda d: str(digits.index(d) if len(d) > 1 else int(d))
    x = list(map(read_digit, re.finditer('(?=([0-9]|one|two|three|four|five|six|seven|eight|nine))', line)))
    print("++", x, int(x[0] + x[-1]))
    return int(x[0] + x[-1])
    #return line

print(sum(map(num, lines)))

print(sum(map(num2, lines)))