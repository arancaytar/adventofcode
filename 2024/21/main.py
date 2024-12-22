import sys
from functools import lru_cache


def read():
    return (sys.stdin.read().strip().split(),)

class opt_dict:
    def __init__(self, data, key):
        self.data = dict(data)
        self.key = key
    def __setitem__(self, key, value):
        if key not in self.data or self.key(self.data[key]) > self.key(value):
            self.data[key] = value

    def __len__(self):
        return len(self.data)

    def __iter__(self):
        return iter(self.data)

    def __getitem__(self, item):
        return self.data[item]

    def items(self):
        return self.data.items()

    def keys(self):
        return self.data.keys()

def solve1(codes):
    numpad_positions = {
        '7': (0,0), '8': (1,0), '9': (2,0),
        '4': (0,1), '5': (1,1), '6': (2,1),
        '1': (0,2), '2': (1,2), '3': (2,2),
        '0': (1,3), 'A': (2,3)
    }
    keypad_positions = {
        '^': (1,0), 'A': (2,0),
        '<': (0,1), 'v': (1,1), '>': (2,1)
    }
    numpad_positions_reverse = {b:a for a,b in numpad_positions.items()}
    keypad_positions_reverse = {b:a for a,b in keypad_positions.items()}


    moves = {
        '^': (0, -1), '>': (1, 0), 'v': (0, 1), '<': (-1, 0)
    }

    def scorefn(d):
        symbols, target = d
        return len(target)

    def solve_code(code):
        states = opt_dict({(numpad_positions['A'], keypad_positions['A'], keypad_positions['A']) : ("", code)}, scorefn)
        while True:
            #display(states)
            new_states = opt_dict({}, scorefn)
            # move r3
            for move, (dx, dy) in moves.items():
                for state in states.keys():
                    r1, r2, (r3x,r3y) = state
                    r3 = (r3x + dx, r3y + dy)
                    if r3 in keypad_positions_reverse:
                        symbols, target = states[state]
                        new_states[r1, r2, r3] = (symbols + move, target) # moved robot r3
            # press A to activate r3
            for state in states.keys():
                r1, r2, r3 = state
                r3_action = keypad_positions_reverse[r3]
                #print(f"R3 presses {r3_action}.")
                if r3_action == 'A': # r3 also presses A
                    r2_action = keypad_positions_reverse[r2]
                    #print(f"R2 presses {r2_action}.")
                    if r2_action == 'A': # r2 also presses A
                        r1_action = numpad_positions_reverse[r1]
                        symbols, target = states[state]
                        #print(f"Managed to press {r1_action} on the numpad.")
                        if r1_action == target[0]: # punching the right number!
                            #print("Success!!")
                            if len(target) == 1:
                                print(symbols + 'A')
                                print(f"Finished after {len(symbols)+1} moves.")
                                return symbols + 'A'
                            new_states[r1,r2,r3] = (symbols + 'A', target[1:])
                            #otherwise, discard this state.
                    else: # r2 moves r1
                        r1x, r1y = r1
                        dx, dy = moves[r2_action]
                        r1 = (r1x+dx, r1y+dy)
                        if r1 in numpad_positions_reverse:
                            symbols, target = states[state]
                            new_states[r1,r2,r3] = (symbols + 'A', target) # moved robot r1
                else: #r3 moves r2
                    r2x, r2y = r2
                    dx, dy = moves[r3_action]
                    r2 =  (r2x+dx, r2y+dy)
                    if r2 in keypad_positions_reverse:
                        #print(f"R2 moves {r3_action} to {keypad_positions_reverse[r2]}.")
                        symbols, target = states[state]
                        new_states[r1,r2,r3] = (symbols + 'A', target) # moved r2
                    #else:
                        #print(f"R2 moves {r3_action} to invalid position {r2}.")
            states = new_states

    def display(states):
        #print(f"State space is {len(states)}")
        for (r1,r2,r3), state in states.items():
            print(f"{numpad_positions_reverse[r1]}{keypad_positions_reverse[r2]}{keypad_positions_reverse[r3]}: {state}")

    return sum(len(solve_code(code)) * int("0"+code[:-1]) for code in codes)

numpad_positions = {
    '7': (0,0), '8': (1,0), '9': (2,0),
    '4': (0,1), '5': (1,1), '6': (2,1),
    '1': (0,2), '2': (1,2), '3': (2,2),
    '0': (1,3), 'A': (2,3)
}
keypad_positions = {
    '^': (1,0), 'A': (2,0),
    '<': (0,1), 'v': (1,1), '>': (2,1)
}
numpad_positions_reverse = {b:a for a,b in numpad_positions.items()}
keypad_positions_reverse = {b:a for a,b in keypad_positions.items()}

pads=[numpad_positions, keypad_positions]

@lru_cache(maxsize=None)
def decide_vertical_first(current, target):
    return True
    # forced:
    if current == '<': # can't go up from <
        return False
    if target == '<': # can't go down to <
        return True
    if current in '147' and target in '0A':
        return False
    if current in '0A' and target in '147':
        return True
    if current in 'A369' and target in '0258147':
        return False
    if current in '0258' and target in '147':
        return False
    if current in '>A' and target in '^v':
        return False
    return True

@lru_cache(maxsize=None)
def get_keypad_presses(current, target, pad):
    vertical_first = decide_vertical_first(current, target)
    x1,y1 = pads[pad][current]
    x2,y2 = pads[pad][target]
    dx,dy = x2-x1,y2-y1
    vertical = ('^v'[dy > 0],)*abs(dy)
    horizontal = ('<>'[dx > 0],) * abs(dx)
    return (vertical + horizontal if vertical_first else horizontal + vertical) + ('A',)

@lru_cache(maxsize=None)
def get_numpad_moves(current, target):
    presses = get_keypad_presses(current,target,0)
    return solve_keypad(presses, 0)

@lru_cache(maxsize=None)
def solve_keypad(presses, depth):
    current_position = 'A'
    moves = ""
    for press in presses:
        moves += get_keypad_moves(current_position, press, depth)
        current_position = press
    return moves

@lru_cache(maxsize=None)
def get_keypad_moves(current, target, depth):
    keypad_presses = get_keypad_presses(current,target,1)
    #print(keypad_presses)
    if depth == 1:
        return "".join(keypad_presses)
        #return len(keypad_presses)
    else:
        return solve_keypad(keypad_presses, depth + 1)

def solve2(codes):
    def solve_code(code):
        current_r1 = 'A'
        moves = ""
        for symbol in code:
            #print(f"Moving on numpad after {moves}: {current_r1} -> {symbol}")
            moves += get_numpad_moves(current_r1, symbol)
            current_r1 = symbol
        print(f"Finished after {len(moves)} moves, {moves}.")
        return moves

    return sum(len(solve_code(code)) * int("0" + code[:-1]) for code in codes)

def main():
    problem = read()
    print(f"Problem 1: {solve1(*problem)}")
    print(f"Problem 2: {solve2(*problem)}")

def test():
    for x in range(100,300):
        problem = ([str(172351**x % 9999) + 'A'],)
        if solve1(*problem) != solve2(*problem):
            print(f"Found discrepancy in {problem}.")
            break

main()
#test()