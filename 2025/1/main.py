import sys

lines = sys.stdin.read().strip().split("\n")
turns = lambda lines: ({'L': -1, 'R': 1}[x[0]] * int(x[1:]) for x in lines)

def sequence(start, turns):
    current = start
    yield current
    for turn in turns:
        current = (current + turn + 100) % 100
        yield current

count1 = lambda value, seq: sum(x == value for x in seq)

#print(list(sequence(50, turns(lines))))
print(count1(0, sequence(50, turns(lines))))

def count2(start, turns):
    current = start
    zeroes = 0
    for i, turn in enumerate(turns):
        print("  ", i, "Turn", current, turn, current + turn)
        if current == 0 and turn < 0: #don't double-count the zero we started on
            print("Turning left from zero")
            zeroes -= 1
        current += turn
        if current <= 0 and current % 100 == 0:
            zeroes += 1
            print("Turned on to zero", zeroes, current)
        while current < 0:
            zeroes += 1
            print("Turned left over zero", zeroes, current)
            current += 100
        while current >= 100:
            zeroes += 1
            print("Turned right over zero", zeroes, current)
            current -= 100
        yield zeroes

def count3(start, turns):
    current = start
    zeroes = 0
    for turn in turns:
        step = 1 if turn > 0 else -1
        for i in range(0, turn, step):
            current += step
            if current % 100 == 0:
                zeroes += 1
        yield zeroes

print(count2(50, turns(lines)))
print(count3(50, turns(lines)))

for i,(x,y) in enumerate(zip(count2(50, turns(lines)), count3(50, turns(lines)))):
    if x != y:
        print(i, x, y)
        break