import numpy as np

class CubeSurface:
    def __init__(self, faces):
        self.position = np.array([1, 1, 0], dtype=int) # top face, top-left corner.
        self.heading = np.array([1, 0, 0], dtype=int) # heading +x.

    def move(self):
        position = self.posi