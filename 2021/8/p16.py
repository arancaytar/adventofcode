from collections import Counter
lengths = Counter()
result = 0
while True:
    try:
        signal, display = input().split(" | ")
        wiring = {i: set("abcdefg") for i in "abcdefg"}
        rev_wiring = {'a': None, 'e': None, 'f': None, 'cf': set(), 'bd': set(), 'dg': set()}
        digits = {frozenset(i): None for i in signal}
        bylength = {i: set() for i in range(8)}
        for x in signal.split():
            bylength[len(x)].add(frozenset(x))
        one, = bylength[2]
        digits[frozenset(one)] = 1
        for i in one:
            wiring[i] &= {'c', 'f'}
            rev_wiring['cf'].add(i)
        four, = bylength[4]
        digits[frozenset(four)] = 4
        for i in four:
            wiring[i] &= {'b', 'c', 'd', 'f'}
            #print(i, wiring[i])
            if {'b', 'd'} <= wiring[i]:
                wiring[i] &= {'b', 'd'}
                rev_wiring['bd'].add(i)
        seven, = tuple(bylength[3])
        digits[frozenset(seven)] = 7
        for i in seven:
            wiring[i] &= {'a', 'c', 'f'}
            if 'a' in wiring[i]:
                wiring[i] &= {'a'}
                rev_wiring['a'] = i
        three, = (x for x in bylength[5] if rev_wiring['cf'] <= x)
        digits[frozenset(three)] = 3
        for i in three:
            wiring[i] &= set("acdfg")
            if {'d', 'g'} <= wiring[i]:
                wiring[i] &= {'d', 'g'}
                rev_wiring['dg'].add(i)
        five, = (x for x in bylength[5] if rev_wiring['bd'] <= x)
        digits[frozenset(five)] = 5
        for i in five:
            wiring[i] &= set("abdfg")
            if wiring[i] == {'f'}:
                rev_wiring['f'] = i
        #print(rev_wiring['cf'] , {rev_wiring['f']})
        rev_wiring['c'], = rev_wiring['cf'] - {rev_wiring['f']}
        wiring[rev_wiring['c']] = {'c'}

        two, = bylength[5] - {three, five}
        digits[frozenset(two)] = 2
        for i in two:
            wiring[i] &= set("acdeg")
            if wiring[i] >= {'e'}:
                wiring[i] &= {'e'}
                rev_wiring['e'] = i
        nine, = (x for x in bylength[6] if rev_wiring['e'] not in x)
        digits[frozenset(nine)] = 9
        six, = (x for x in bylength[6] - {nine} if rev_wiring['c'] not in x)
        digits[frozenset(six)] = 6
        zero, = bylength[6] - {six, nine}
        digits[frozenset(zero)] = 0
        eight, = bylength[7]
        digits[frozenset(eight)] = 8
        result += int("".join(str(digits[frozenset(x)]) for x in display.split()))
    except EOFError:
        break
print(result)