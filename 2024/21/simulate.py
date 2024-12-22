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
import sys

def simulate(s):
    r1, r2, r3 = 'A', 'A', 'A'
    print(f"State {r1}{r2}{r3}")
    output = ""
    for i, symbol in enumerate(s):
        print(f"    Taking manual action {symbol}")
        if symbol == 'A':
            print(f"    Activating r3={r3}")
            if r3 == 'A':
                print(f"    Activating r2={r2}")
                if r2 == 'A':
                    output += r1
                    print(f"    Emitting {r1} after command sequence {s[:i+1]}")
                else:
                    r1x,r1y = numpad_positions[r1]
                    dx, dy = moves[r2]
                    r1 = numpad_positions_reverse[r1x+dx,r1y+dy]
                    print(f"    Moving r1 to {r1}")
            else:
                r2x,r2y = keypad_positions[r2]
                dx,dy = moves[r3]
                r2 = keypad_positions_reverse[r2x + dx, r2y + dy]
                print(f"    Moving r2 to {r2}")
        else:
            r3x, r3y = keypad_positions[r3]
            dx, dy = moves[symbol]
            r3 = keypad_positions_reverse[r3x + dx, r3y + dy]
            print(f"    Moving r3 to {r3}")
        print(f"New state {r1}{r2}{r3}")
    return output

for line in sys.stdin.read().strip().split():
    print(simulate(line))