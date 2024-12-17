import sys

def solve1(data):
    numbers = list(map(int, data.split()))
    numbers = shuffle(numbers)
    n = len(numbers)
    zero = numbers.index(0)
    return sum(numbers[(zero + i) % n] for i in (1000, 2000, 3000))

def solve2(data):
    numbers = list(map(int, data.split()))
    numbers = [811589153 * x for x in numbers]
    numbers = shuffle2(numbers)
    n = len(numbers)
    zero = numbers.index(0)
    return sum(numbers[(zero + i) % n] for i in (1000, 2000, 3000))


def shuffle(numbers):
    numbers = [[x, bool(x)] for x in numbers]
    index = 0
    n = len(numbers)
    while index < n:
        print(index)
        m = numbers[index]
        if m[1]:
            m[1] = False
            new_index = (index + m[0] + (n-1)) % (n-1)
            print(f"Moving {m} from {index} to {new_index}.")
            if new_index > index:
                numbers = numbers[:index] + numbers[index+1:new_index+1] + [m] + numbers[new_index+1:]
                # no change to index - next element has shifted forward.
            else:
                numbers = numbers[:new_index] + [m] + numbers[new_index:index] + numbers[index+1:]
                index += 1
                # advance index - elements ahead have not shifted.
        else:
            index += 1
        #print(numbers)
    return [x for x,y in numbers]

def shuffle2(numbers):
    original = [[x, i] for i, x in enumerate(numbers)]
    shuffled = [[x, i] for i, x in enumerate(numbers)]

    n = len(original)

    for i in range(10):
        for m in original:
            old_index = m[1]
            new_index = (old_index + m[0] + n - 1) % (n - 1)
            if new_index > old_index:
                shuffled[old_index:new_index + 1] = (
                        shuffled[old_index + 1:new_index + 1] +
                        shuffled[old_index:old_index + 1]
                )
                # update indices.
                for j in range(old_index, new_index + 2):
                    original[shuffled[j][1]][1] = j
            elif new_index < old_index:
                shuffled[new_index:old_index + 1] = (
                        shuffled[old_index:old_index + 1] +
                        shuffled[new_index:old_index]
                )
                # update indices.
                for j in range(new_index, old_index + 1):
                    original[shuffled[j][1]][1] = j

    return [m[0] for m in shuffled]

data = sys.stdin.read()
#print(solve1(data))
print(solve2(data))