import sys

numbers = map(int, input().split(","))
boards = list(map(int, sys.stdin.read().split()))

def won(boards):
    for i in range(0, len(boards), 25):
        if any(sum(boards[i+5*j:i+5*j+5]) == -5 or sum(boards[i+j:i+25:5]) == -5 for j in range(5)):
            yield i, sum(map(lambda x:max(x, 0), boards[i:i+25]))

def apply(boards, num):
    for i, c in enumerate(boards):
        if c == num:
            boards[i] = -1

def pr(boards):
    for i in range(0, len(boards), 25):
        print("\n".join("\t".join(map(str, boards[i+j:i+j+5])) for j in range(0, 25, 5)))
        print("---")

prev = set()
for num in numbers:
    apply(boards, num)
    #print(f"Number is {num}")
    #pr(boards)
    y = dict(won(boards))
    new, prev = y.keys() - prev, y.keys()
    if len(y) * 25 == len(boards):
        print(max(y[i] for i in new) * num)
        break