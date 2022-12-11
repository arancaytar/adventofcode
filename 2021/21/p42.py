from collections import defaultdict
from functools import reduce

def diracdie():
    return {1:1, 2:1, 3:1}

def apply(states, outcomes):
    new_states = defaultdict(int)
    for state, count in states.items():
        for outcome, count2 in outcomes.items():
            new_states[state + outcome] += count * count2
    return new_states


diractriple = reduce(apply, [diracdie()]*3, {0:1})

def triple(turn):
    return {(turn, roll): count for roll, count in diractriple.items()}

def take(k,z):
    yield from (x for i,x in zip(range(k), z))



class State:
    def __init__(self, p1, p2, s1, s2):
        self.state = (p1, p2, s1, s2)

    def __hash__(self):
        return hash(self.state)

    def __eq__(self, other: 'State'):
        return self.state == other.state

    def __add__(self, t):
        turn, roll = t
        write = list(self.state)
        write[turn] = (write[turn] + roll) % 10 or 10
        write[2+turn] += write[turn]
        return State(*write)

    def won(self):
        if self.state[2] >= 21:
            return 1
        elif self.state[3] >= 21:
            return 2

    def __repr__(self):
        return str(self.state)

def game(p1, p2):
    states = {State(p1, p2, 0, 0): 1}
    endings = {1: 0, 2: 0}
    turn = 0
    while states:
        new_states = {}
        for state, count in apply(states, triple(turn)).items():
            ending = state.won()
            if ending:
                endings[ending] += count
            else:
                new_states[state] = count
        #print(endings, new_states)
        #input()
        print(endings)
        states = new_states
        turn = 1-turn
    return max(endings.values())

#print(game(4, 8))
print(game(7, 9))

