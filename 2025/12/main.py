import sys
import grid
def read():
    def read_shape(s):
        return grid.Grid.read(s[3:], lambda x:x == '#')

    def read_region(s):
        s = s.split()
        presents = list(map(int, s[1:]))
        size = tuple(map(int, s[0][:-1].split("x")))
        return size, presents

    chunks = sys.stdin.read().strip().split("\n\n")
    shapes = list(map(read_shape, chunks[:-1]))
    regions = list(map(read_region, chunks[-1].split("\n")))
    return shapes, regions

def solve1(shapes, regions):
    sizes = [s.grid.sum() for s in shapes]
    return sum(w*h >= sum(size * count for size, count in zip(sizes, presents)) for ((w, h), presents) in regions)


def main():
    shapes, regions = read()
    print(solve1(shapes, regions))

main()