import math
from datetime import date
import numpy as np
from PIL import Image
from distinctipy import distinctipy
from src.piece import Piece
from src.exceptions import UnplaceablePiece

BOARD = [
    [0, 0, 0, 0, 0, 0, 1],
    [0, 0, 0, 0, 0, 0, 1],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 0, 0, 0],
]

class Board:
    def __init__(self, input_date, solution_count=16):
        self.board = self.generate_board(input_date)
        self.grid_size = int(math.ceil(math.sqrt(solution_count)))
        self.solutions = np.full((self.grid_size * 8 + self.grid_size - 1, self.grid_size * 7 + self.grid_size - 1), 0)
        self.solution_index = 0
        self.placed_pieces = []
        self.next_position = (-1, -1)
        self._set_next_position()

    def place_piece(self, piece: Piece):
        height, width = piece.current_shape.data.shape
        board_x = self.next_position[0]
        board_y = self.next_position[1] - piece.current_shape.offset
        placement_location = np.index_exp[board_x: board_x + height, board_y: board_y + width]
        mask = self.board[placement_location]
        if mask.shape != piece.current_shape.data.shape:
            raise UnplaceablePiece
        merged = mask + piece.current_shape.data
        if np.max(merged) > 1:
            raise UnplaceablePiece
        self.board[placement_location] = merged
        piece.placement_location = placement_location
        self.placed_pieces.append(piece)
        self._set_next_position()

    def pop_piece(self):
        temp_board = np.zeros(self.board.shape, dtype=int)
        last_piece: Piece = self.placed_pieces.pop()
        temp_board[last_piece.placement_location] = last_piece.current_shape.data
        self.board -= temp_board
        self._set_next_position()

    def _set_next_position(self):
        self.next_position = np.unravel_index(np.argmin(self.board), self.board.shape)

    def store_solution(self):
        board_template = self.board.copy()
        d, m = divmod(self.solution_index, self.grid_size)
        offset_x = d * (8 + 1)
        offset_y = m * (7 + 1)
        for i, piece in enumerate(self.placed_pieces):
            board_template[piece.placement_location] += piece.current_shape.data * (i + 2)
        offset_location = np.index_exp[offset_x: offset_x + 8, offset_y: offset_y + 7]
        self.solutions[offset_location] = board_template
        self.solution_index += 1

    def print_picture(self):
        colors = [(210, 210, 210), (0, 0, 0)] + distinctipy.get_colors(11)
        colors = [distinctipy.get_rgb256(c) for c in colors]
        target_width = 700
        target_height = 800
        image_array = np.take(colors, self.solutions, axis=0)
        original_height, original_width, _ = image_array.shape
        width_scale = target_width // original_width
        height_scale = target_height // original_height
        scaled_array = np.repeat(np.repeat(image_array, width_scale, axis=1), height_scale, axis=0)
        im = Image.fromarray(scaled_array.astype(np.uint8))
        im.show()

    def print(self):
        print(self.board)

    @staticmethod
    def generate_board(input_date: date):
        """Generate numpy matrix for the board by hiding 3 cells corresponding to input date."""
        board_template = np.array(BOARD)
        month_x, month_y = divmod(input_date.month - 1, 6)
        day_x, day_y = divmod(input_date.day - 1, 7)
        day_x += 2
        weekday = input_date.weekday()
        if weekday == 6:
            weekday_x, weekday_y = 6, 3
        else:
            weekday_x, weekday_y = divmod(weekday, 3)
            weekday_x += 6
            weekday_y += 4
        board_template[month_x][month_y] = 1
        board_template[day_x][day_y] = 1
        board_template[weekday_x][weekday_y] = 1
        return board_template
