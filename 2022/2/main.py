import sys

scores = 0
try:
    while True:
        x, y = input().split()
#        score = {'X': 1, 'Y': 2, 'Z': 3}[y] + {
#            'AY': 6, 'BZ': 6, 'CX': 6,
#            'AZ': 0, 'BX': 0, 'CY': 0,
#            'AX': 3, 'BY': 3, 'CZ': 3
#        }[x + y]
        score = {
            'AY': 4, 'BY': 5, 'CY': 6,
            'AZ': 8, 'BZ': 9, 'CZ': 7,
            'AX': 3, 'BX': 1, 'CX': 2
          }[x + y]
        print(score)
        scores += score
except:
    pass




print(scores)