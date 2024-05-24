# standard library imports
from typing import List, Optional

# third party imports
from sty import bg, fg

# local imports


def print_board(colors: List[List[str]], solution: Optional[List[int]] = None) -> None:
    N = len(colors)
    sep = "\n" + "+---" * N + "+\n"
    board = sep

    if solution:
        for row, queen_pos in zip(colors, solution):
            board_row = "|"
            for i, cell in enumerate(row):
                r, g, b = [int(x) for x in cell.split(",")]
                if i == queen_pos:
                    board_row += (
                        bg(r, g, b) + " " + fg.black + "Q" + fg.rs + " " + bg.rs + "|"
                    )
                else:
                    board_row += bg(r, g, b) + "   " + bg.rs + "|"
            board += board_row + sep
    else:
        for row in colors:
            board_row = "|"
            for cell in row:
                r, g, b = [int(x) for x in cell.split(",")]
                board_row += bg(r, g, b) + "   " + bg.rs + "|"
            board += board_row + sep

    print(board + "\n")
