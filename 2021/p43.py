import numpy as np

def clamp(x,low,high):
    return min(max(x, low), high)

def main():
    cubes = np.zeros((101,101,101), dtype=bool)

    while True:
        try:
            state, coords = input().split(" ")
            state = state == 'on'
            (x1, x2), (y1, y2), (z1, z2) = (map(int, x.split("=")[1].split("..")) for x in coords.split(","))
            X = range(clamp(x1,-50,51)+50,clamp(x2,-51,50)+51)
            Y = range(clamp(y1,-50,51)+50, clamp(y2,-51,50)+51)
            Z = range(clamp(z1,-50,51)+50, clamp(z2,-51,50)+51)
            print(X,Y,Z)
            for x in X:
                for y in Y:
                    for z in Z:
                        cubes[x,y,z] = state
        except EOFError:
            return cubes.sum()

print(main())