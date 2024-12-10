import sys
import math
import numpy as np
import heapq

def read():
    return (list(map(int, sys.stdin.read().strip())),)

def solve1(numbers):
    disk = np.full(sum(numbers), -1, dtype=int)
    a = 0
    for i, number in enumerate(numbers):
        if i % 2 == 0:
            disk[a:a + number] = i // 2
        a += number
        
    a, b = 0, len(disk) - 1
    while a < b or disk[b] < 0:
        if disk[a] >= 0:
            a += 1
        elif disk[b] < 0:
            b -= 1
        else:
            disk[a] = disk[b]
            disk[b] = -1
            a += 1
            b -= 1
#    print("".join(map(str, disk[:b+1])))
    checksum = 0
    for i in range(b + 1):
        checksum += i * int(disk[i])
#    return sum(i * x * (x > 0) for i, x in enumerate(disk))
    return checksum
   
def solve2(numbers):
    files = []
    space_index = [[] for i in range(10)]
    a = 0
    # Find files and spaces, group the latter by size
    for i, number in enumerate(numbers):
        if i % 2 == 0:
            files.append((i//2, number, a))
        else:
            space_index[number].append(a)
        a += number

    for i in range(10):
        heapq.heapify(space_index[i])

    max_space_remaining = len(space_index) - 1

    # Iterate through files from right to left
    for i in range(len(files) - 1, -1, -1):
        file_id, file_size, position = files[i]
        # Find the first eligible space:
        available_sizes = list(filter(lambda s: space_index[s], range(file_size, 10)))
        if available_sizes:
            size = min(available_sizes, key=lambda s:space_index[s][0])
            # Move file into this space and remove space from the index.
            s = heapq.heappop(space_index[size])
            if s < position:
                # only move files further left (otherwise, no file will still use this space because all future files will be even further right)
                files[i] = (file_id, file_size, s)
                # Add the remaining, smaller space to the index.
                if size > file_size:
                    heapq.heappush(space_index[size - file_size], s + file_size)
    
    checksum = 0
    for file_id, file_size, start in files:
        end = start + file_size - 1
        checksum += file_id * ((end * (end + 1)) - ((start * (start - 1)))) // 2
    return checksum
  
def main():
    problem = read()
    print(f"Problem 1: {solve1(*problem)}")
    print(f"Problem 2: {solve2(*problem)}")

def debug():
    return None
    

main()
#debug()