import sys
import re
solution = None

def s1(line):
    pass

def read_tree(lines):
    tree = {'/':{}}
    current_path = []
    entries = []
    for line in lines:
        if line[0] == '$':
            if line[:5] == '$ cd ':
                target = line[5:]
                current_path = change_dir(current_path, target)
            elif line == '$ ls':
                entries = get_dir(tree, current_path)
        else:
            size, name = line.split()
            if size == 'dir':
                size = {}
            else:
                size = int(size)
                name = 'FILE_' + name
            entries[name] = size
    return tree

def get_dir(tree, path):
    for x in path:
        tree = tree[x]
    return tree

def get_sizes(tree, dirs, current):
    total_size = 0
    for x,y in tree.items():
        if type(y) is int:
            total_size += y
        else:
            total_size += get_sizes(y, dirs, x)
    dirs.append(total_size)
    return total_size

def solve1(data):
    lines = data.split("\n")
    tree = read_tree(lines)
    print(tree)
    dir_sizes = []
    get_sizes(tree['/'], dir_sizes, '/')
    return sum(size for size in dir_sizes if size <= 100000)


def change_dir(current_path, target):
    if target == '/':
        return ['/']
    elif target == '..':
        return current_path[:-1]
    else:
        return current_path + [target]

def s2(line):
    pass

def solve2(data):
    lines = data.split("\n")
    tree = read_tree(lines)
    print(tree)
    dir_sizes = []
    total_size = get_sizes(tree['/'], dir_sizes, '/')

    free = 70000000 - total_size
    needed = 30000000 - free

    solution = min(size for size in dir_sizes if size >= needed)


    return solution



#print(read_move('move 1 from 2 to 3'))
data = sys.stdin.read().strip()

#print(solve1(data))
print(solve2(data))