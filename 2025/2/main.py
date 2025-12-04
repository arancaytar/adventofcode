import sys

ranges = [tuple(x.split("-")) for x in sys.stdin.read().strip().split(",")]

def next_invalid_root(n):
    k = len(n)
    if k % 2 == 0: # if n has an even digit count, copy the first half
        root = n[:k//2]
        if int(root + root) < int(n): # if the result is smaller, increment by 1.
            # we know that the result must be greater than n.
            root = str(int(root) + 1)
    else: # if n has an odd digit count, the next invalid is (10*)\1
        root = "1" + "0"*(k//2)
    return root

def next_invalid_root2(n, c):
    k = len(n)
    if k % c == 0: # if k is divisible by c, copy the first segment
        root = n[:k//c]
        if int(root * c) < int(n): # if the result is smaller, increment by 1.
            # we know that the result must be greater than n.
            root = str(int(root) + 1)
    else: # if n is not divisible by c, the next invalid is (10*)\1{c-1} of the proper length
        root = "1" + "0"*(k//c)
    return root

def prev_invalid_root(n):
    k = len(n)
    if k % 2 == 0:
        root = n[:k//2]
        if int(root + root) > int(n):
            root = str(int(root) - 1)
    elif k > 1: # if n has an odd digit count, the last invalid root is (9+)\1
        root = "9"*(k//2)
    else:
        root = "0" # avoid int('') error
    return root

def prev_invalid_root2(n, c):
    k = len(n)
    if k % c == 0:
        root = n[:k//c]
        if int(root * c) > int(n):
            root = str(int(root) - 1)
    elif k > c: # if n has an odd digit count, the last invalid root is (9+)\1
        root = "9"*(k//c)
    else:
        root = "0" # avoid int('') error
    return root


def range_invalids(a, b):
    x = int(next_invalid_root(a))
    y = int(prev_invalid_root(b))
    yield from (int(str(r)*2) for r in range(x, y + 1, 1))

def range_invalids2(a, b):
    for c in range(2, max(len(a), len(b)) + 1):
        x = int(next_invalid_root2(a, c))
        y = int(prev_invalid_root2(b, c))
        #print(f"with {c} repetitions: {x} ... {y}")
        yield from (int(str(r)*c) for r in range(x, y + 1, 1))


def main1(ranges):
    #for range in ranges:
    #    print(range)
    #    for i in range_invalids(*range):
    #        print("   ", i)
    return sum(i for range in ranges for i in range_invalids(*range))

def main2(ranges):
    #for range in ranges:
        #print(range)
        #for i in range_invalids2(*range):
            #print("   ", i)
    return sum(set(i for range in ranges for i in range_invalids2(*range)))



print(main1(ranges))
print(main2(ranges))


# it's lower than 52317623584
