import sys

numbers = map(int, input().split(","))
boards = list(map(int, sys.stdin.read().split()))

def won(boards):
    for i in range(0, len(boards), 25):
        if any(sum(boards[i+5*j:i+5*j+5]) == -5 or sum(boards[i+j:i+25:5]) == -5 for j in range(5)):
            yield sum(map(lambda x:max(x, 0), boards[i:i+25]))

def apply(boards, num):
    for i, c in enumerate(boards):
        if c == num:
            boards[i] = -1

def pr(boards):
    for i in range(0, len(boards), 25):
        print("\n".join("\t".join(map(str, boards[i+j:i+j+5])) for j in range(0, 25, 5)))
        print("---")

for num in numbers:
    apply(boards, num)
    #print(f"Number is {num}")
    #pr(boards)
    y = set(won(boards))
    #print(y)
    if y:
        print(max(y) * num)
        break