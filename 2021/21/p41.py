def detdie():
    state = 1
    while True:
        yield state or 100
        state = (state + 1) % 100


def take(k,z):
    yield from (x for i,x in zip(range(k), z))


def triple(z):
    return sum(take(3, z))

def game(die, p1, p2):
    pos = [p1, p2]
    scores = [0,0]
    turns = 0
    print(turns, pos, scores)
    while max(scores) < 1000:
        t = turns % 2
        pos[t] = ((pos[t] + triple(die)) % 10) or 10
        scores[t] += pos[t]
        turns += 1
        print(turns, pos, scores)
    return turns*3*min(scores)

#print(game(detdie(), 4, 8))
print(game(detdie(), 7, 9))