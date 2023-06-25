# Recursive solver of the puzzle.
from src.exceptions import UnplaceablePiece, DesiredSolutionsFound


def solver(board, pieces, solution_count):
    if board.solution_index == solution_count:
        raise DesiredSolutionsFound
    if len(pieces) == 0:
        print(f"\rFound {board.solution_index + 1} solution(s).", end='')
        board.store_solution()
    count = len(pieces)
    for i in range(count):
        piece = pieces.pop(0)
        for piece_shape in piece:
            try:
                board.place_piece(piece_shape)
            except UnplaceablePiece:
                continue
            solver(board, pieces, solution_count)
            board.pop_piece()
        pieces.append(piece)