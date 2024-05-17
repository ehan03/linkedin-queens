# standard library imports
from typing import List, Set

# third party imports

# local imports


class LinkedInQueensSolver:
    """
    Class to brute force the daily LinkedIn Queens game
    """

    def __init__(self, board: List[List[str]]) -> None:
        self.board = board
        self.board_size = len(board)
        self.solution = []

    def __get_solutions(self, arr: List[int], seen_colors: Set) -> None:
        if len(arr) == self.board_size:
            self.solution.append(arr)
            return

        for i in range(self.board_size):
            if (not arr) or (
                i not in arr
                and abs(arr[-1] - i) != 1
                and self.board[len(arr)][i] not in seen_colors
            ):
                self.__get_solutions(arr + [i], seen_colors | {self.board[len(arr)][i]})

    def solve(self) -> List[int]:
        self.__get_solutions([], set())

        if not self.solution:
            raise ValueError("No solution found")

        return self.solution[0]
