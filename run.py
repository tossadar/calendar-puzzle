import datetime
import argparse
from src.piece import *
from src.board import Board
from src.solver import solver
from src.exceptions import DesiredSolutionsFound


def main():
    parser = argparse.ArgumentParser(description='Process arguments')
    parser.add_argument('--solutions_count', '--sc', type=int, default=4, help='Number of solutions')
    args = parser.parse_args()
    solutions_count = args.solutions_count
    date_format = "YYYY-MM-DD"
    print("Calendar puzzle. Enter 'exit' to shutdown")
    while True:
        input_date = datetime.datetime.now().date()
        prompt = input(f"\nEnter date in following format: {date_format} ({input_date}): ")
        if prompt == 'exit':
            exit()
        if prompt != "":
            try:
                input_date = datetime.datetime.strptime(prompt, "%Y-%m-%d").date()
            except ValueError:
                print(f"Wrong date format. Please use {date_format} format.")
                continue
        calendar_board = Board(input_date, solutions_count)
        all_pieces = [L, N, P, T, U, V, Z, J, I, S]
        print(f"Looking for {solutions_count} solutions!")
        try:
            solver(calendar_board, all_pieces, solutions_count)
        except DesiredSolutionsFound:
            pass
        calendar_board.print_picture()


if __name__ == '__main__':
    main()
