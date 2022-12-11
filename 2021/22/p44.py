import operator
from functools import reduce


class VoxelTree:
    pass

# take two ranges A and B and return three sets of disjoint ranges:
# one containing ranges whose union is A \ B.
# one whose union is A & B
# one whose union is B \ A.
def rectify_ranges(r1: range, r2: range, keep_intersect = True) -> (set, set, set):
    if r1 == r2:
        # ranges are equal.
        return (set(), {r1}, set()) if keep_intersect else ({r1}, set(), set())

    if r1.start < r2.start:
        # disjoint
        if r1.stop <= r2.start:
            return {r1}, set(), {r2}
        # overlap
        if r1.stop < r2.stop:
            return (
                {range(r1.start, r2.start)}, # part only in A
                {range(r2.start, r1.stop)}, # part in intersection
                {range(r1.stop, r2.stop)} # part only in B
            ) if keep_intersect else ({range(r1.start, r1.stop)}, set(), {range(r1.stop, r2.stop)})
        # r1 fully contains r2.
        return (
            {range(r1.start, r2.start), range(r2.stop, r1.stop)},
            {r2},
            set()
        ) if keep_intersect else ({r1}, set(), set())
    if r1.start == r2.start:
        # r2 fully contains r1.
        if r1.stop < r2.stop:
            return (set(), {r1}, {range(r1.stop, r2.stop)}) if keep_intersect else (set(), set(), {r2})

    # either r1.start > r2.start, or r1.start == r2.start and r1.stop > r2.stop.
    # swap operands and swap outer sets
    a, b, c = rectify_ranges(r2, r1)
    return c, b, a

def rectify_cuboids(c1: (range, range, range), c2: (range, range, range), avoid_intersect=False):
    (x1, y1, z1), (x2, y2, z2) = c1, c2
    ax, bx, cx = rectify_ranges(x1, x2, avoid_intersect)
    ay, by, cy = rectify_ranges(y1, y2, avoid_intersect)
    az, bz, cz = rectify_ranges(z1, z2, avoid_intersect)
    # cuboids only in A
    return (
        ({(x, y, z) for x in ax for y in ay for z in az} |
         {(x, y, z) for x in ax for y in ay for z in bz} |
         {(x, y, z) for x in ax for y in by for z in az} |
         {(x, y, z) for x in ax for y in by for z in bz} |
         {(x, y, z) for x in bx for y in ay for z in az} |
         {(x, y, z) for x in bx for y in ay for z in bz} |
         {(x, y, z) for x in bx for y in by for z in az}
         ),
        # cuboids in A and B.
        {(x,y,z) for x in bx for y in by for z in bz},
        ({(x, y, z) for x in cx for y in cy for z in cz} |
         {(x, y, z) for x in cx for y in cy for z in bz} |
         {(x, y, z) for x in cx for y in by for z in cz} |
         {(x, y, z) for x in cx for y in by for z in bz} |
         {(x, y, z) for x in bx for y in cy for z in cz} |
         {(x, y, z) for x in bx for y in cy for z in bz} |
         {(x, y, z) for x in bx for y in by for z in cz}
         ),
    )

#print(rectify_cuboids(
#    (range(10, 21), range(10, 21), range(100, 200)),
#    (range(5, 26), range(5, 26), range(125, 175))
#))


class RangeSet:
    def __init__(self, r:range):
        # Range sets are directionless, so invert if step size is negative.
        if r.step < 0:
            r = range(r.stop-1, r.start+1, -r.step)
        self.r = r

    def __and__(self, other):
        if isinstance(other, range):
            return self & RangeSet(other)

        step = self.r.step

        if step != other.r.step:
            raise ValueError("Steps must be equal.")

        start = max(self.r.start, other.r.start)
        stop = min(self.r.stop, other.r.stop)

        return RangeSet(range(start, stop, step))

    def __or__(self, other):
        if isinstance(other, range):
            return self | RangeSet(other)

        if self.r.step != other.r.step:
            raise ValueError("Range steps must be equal for union.")

        if step % min(self.r.step, other.r.step):
            raise ValueError("One range step must divide the other for intersection.")

        start = max(self.r.start, other.r.start)
        stop = min(self.r.stop, other.r.stop)

        return RangeSet(range(start, stop, step))

def product(z):
    return reduce(operator.mul, z, 1)

def cuboid_size(c1: (range, range, range)):
    return product(map(len, c1))

def main():
    active_cuboids = set()
    while True:
        try:
            state, coords = input().split(" ")
            state = state == 'on'
            (x1, x2), (y1, y2), (z1, z2) = (map(int, x.split("=")[1].split("..")) for x in coords.split(","))
            cuboids = {(range(x1, x2+1), range(y1, y2+1), range(z1, z2+1))}
            new_active_cuboids = set()
            for active_cuboid in active_cuboids:
                new_cuboids = set()
                for new_cuboid in cuboids:
                    a, b, c = rectify_cuboids(active_cuboid, new_cuboid, state)
                    # a and b are already active, thus disjoint with other existing cuboids.
                    new_active_cuboids |= a
                    # only add the intersect if we are switching it on
                    if state:
                        new_active_cuboids |= b
                        # c is newly added, and thus disjoint with other newly added cuboids.
                    new_cuboids |= c
                cuboids = new_cuboids
            # only add the new disjoint cuboids if we are switching them on.
            if state:
                new_active_cuboids |= cuboids
            active_cuboids = new_active_cuboids
            print(len(active_cuboids), sum(map(cuboid_size, active_cuboids)))
        except EOFError:
            return

print(main())