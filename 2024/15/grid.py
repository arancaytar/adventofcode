import numpy as np

class Grid:
    def __copy__(self):
        return Grid(copy(self.grid))

    def __init__(self, data: np.array):
        self.grid = data
        (self.width, self.height) = self.grid.shape

    @staticmethod
    def read(str, key=None):
        # read the input data as line-separated characters, but store by columns for x,y indexing.
        grid = np.array([list(row) for row in data.strip().split("\n")], dtype=str).transpose()

        if key is not None:
            key = np.vectorize((lambda x: key[x]) if type(key) is dict else key)
            grid = key(grid)
        return Grid(grid)

    def __getitem__(self, idx):
        return self.grid[idx]
    
    def __setitem__(self, idx, val):
        self.grid[idx] = val

    def __iter__(self):
        for x in range(self.width):
            for y in range(self.height):
                yield (x, y), self[x,y]

    def neighbors(self, x, y, neighborhood, borders=False):
        for dx, dy in neighborhood:
            x2, y2 = x + dx, y + dy
            if not (0 <= x2 < self.width and 0 <= y2 < self.height):
                if borders:
                    x2, y2 = x2 + self.shape[0] % self.shape[0], y2 + self.shape[1] % self.shape[1]
                else:
                    continue
            yield (x2, y2), self[x2, y2]

    def neighbors4(self, x, y, borders=False):
        return self.neighbors(x, y, ((1, 0), (0, 1), (-1, 0), (0, -1)), borders)

    def neighbors8(self, x, y, borders=False):
        return self.neighbors(x, y, ((-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0)), borders)
