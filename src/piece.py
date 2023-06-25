# piece module
import numpy as np


class Shape:
    def __init__(self, shape: np.ndarray):
        self.data = shape
        self.offset = np.argmax(self.data)


class Piece:
    def __init__(self, shape: np.ndarray, current_index=0, name="Unnamed"):
        self.shapes = []
        self._precompute(shape)
        self.current_index = current_index
        self.current_shape = self.shapes[self.current_index]
        self.name = name
        self.placement_location = None

    def _precompute(self, shape):
        # Generate all 8 combinations and store them in the result array
        for i in range(4):
            rotated_matrix = np.rot90(shape, k=i)
            flipped_matrix = np.fliplr(rotated_matrix)
            if not any(np.array_equal(rotated_matrix, shape.data) for shape in self.shapes):
                self.shapes.append(Shape(rotated_matrix))
            if not any(np.array_equal(flipped_matrix, shape.data) for shape in self.shapes):
                self.shapes.append(Shape(flipped_matrix))

    def print(self):
        for shape in self.shapes:
            print(shape.data)

    def __repr__(self):
        return f"<Piece: {self.name}, Shape: \n{self.current_shape.data}>"

    def __str__(self):
        return self.name

    def __iter__(self):
        return self

    def __next__(self):
        self.current_index += 1
        try:
            self.current_shape = self.shapes[self.current_index - 1]
            return self
        except IndexError:
            self.current_index = 0
            raise StopIteration  # Done iterating.


# Tetrominos
J = Piece(np.array([
    [1, 0, 0],
    [1, 1, 1]
]), name="J-tetromino")

I = Piece(np.array([
    [1, 1, 1, 1]
]), name="I-tetromino")

S = Piece(np.array([
    [1, 1, 0],
    [0, 1, 1]
]), name="S-tetromino")

# Pentominos
L = Piece(np.array([
    [1, 0, 0, 0],
    [1, 1, 1, 1]
]), name="L-pentomino")

N = Piece(np.array([
    [1, 1, 0, 0],
    [0, 1, 1, 1]
]), name="N-pentomino")

P = Piece(np.array([
    [1, 1, 0],
    [1, 1, 1]
]), name="P-pentomino")

T = Piece(np.array([
    [1, 1, 1],
    [0, 1, 0],
    [0, 1, 0]
]), name="T-pentomino")

U = Piece(np.array([
    [1, 0, 1],
    [1, 1, 1]
]), name="U-pentomino")

V = Piece(np.array([
    [1, 0, 0],
    [1, 0, 0],
    [1, 1, 1]
]), name="V-pentomino")

Z = Piece(np.array([
    [1, 1, 0],
    [0, 1, 0],
    [0, 1, 1]
]), name="Z-pentomino")

