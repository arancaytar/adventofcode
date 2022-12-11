import collections
import sys
import re
from collections import deque
from collections import Counter
solution = None

def s1(line):
    pass

def parse(text):
    monkeys = text.split("\n\n")
    return [parse_monkey(m) for m in monkeys]

def parse_monkey(text):
    lines = text.split("\n")
    print(lines)
    start = deque(map(int, lines[1][len('  Starting items: '):].split(", ")))
    op = lines[2][len('  Operation: new = '):].split()
    test = int(lines[3][len('  Test: divisible by '):])
    true = int(lines[4][len('    If true: throw to monkey '):])
    false = int(lines[5][len('    If false: throw to monkey '):])
    return {'items': start, 'op': op, 'test': test, 'targets': [false, true]}

def solve1(data):
    monkeys = parse(data)
    counter = Counter()
    for i in range(20):
        for j,monkey in enumerate(monkeys):
            while monkey['items']:
                counter[j] += 1
                item = apply_op(monkey['items'].popleft(), monkey['op'])
                #print('Checking',item)
                item = item // 3
                #print('Relieved',item)
                result = item % monkey['test'] == 0
                #print('Result is',result)
                #print('Target is',monkey['targets'][result])
                monkeys[monkey['targets'][result]]['items'].append(item)
    #print(counter)
    a,b = counter.most_common(2)
    return a[1]*b[1]
def apply_op(item, op):
    a,operator,b = op
    if a == 'old':
        a = item
    else:
        a = int(a)
    if b == 'old':
        b = item
    else:
        b = int(b)
    #print('Inspect  ', item)
    if operator == '*':
        return a*b
    elif operator == '+':
        return a+b

def s2(line):
    pass

def solve2(data):
    monkeys = parse(data)
    global_mod = 1
    for x in monkeys:
        global_mod *= x['test']

    counter = Counter()
    for i in range(10000):
        for j, monkey in enumerate(monkeys):
            while monkey['items']:
                counter[j] += 1
                item = apply_op(monkey['items'].popleft(), monkey['op'])
                # print('Checking',item)
                item = item % global_mod
                # print('Relieved',item)
                result = item % monkey['test'] == 0
                # print('Result is',result)
                # print('Target is',monkey['targets'][result])
                monkeys[monkey['targets'][result]]['items'].append(item)
    # print(counter)
    a, b = counter.most_common(2)

    return a[1] * b[1]


#print(read_move('move 1 from 2 to 3'))
data = sys.stdin.read().strip()

print(solve1(data))
print(solve2(data))