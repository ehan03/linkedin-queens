# standard library imports
import os
import sys

os.system("")
sys.path.append(".")

# third party imports
import numpy as np
import pyautogui
from mss import mss

# local imports
from src import GridExtractor, LinkedInQueensSolver
from src.constants import WINDOW_HEIGHT, WINDOW_WIDTH
from src.utils import print_board


def main() -> None:
    """
    Main function
    """

    extractor = GridExtractor()
    monitor = {
        "top": 0,
        "left": 0,
        "width": WINDOW_WIDTH,
        "height": WINDOW_HEIGHT,
    }

    with mss() as sct:
        while True:
            image = sct.grab(monitor)
            image = np.array(image)
            is_present = extractor.check_template(image)

            if is_present:
                break

    colors, centers = extractor.extract_grid(
        top_offset=monitor["top"], left_offset=monitor["left"]
    )
    if not colors and not centers:
        print("Black pixels found in cell centers. Did you already solve the puzzle?")
    else:
        print("Detected game board:")
        print_board(colors=colors)

        solver = LinkedInQueensSolver(colors)
        solution = solver.solve()

        print("Solution:")
        print_board(colors=colors, solution=solution)

        for idx, row in zip(solution, centers):
            target_coords = row[idx]
            pyautogui.click(x=target_coords["x"], y=target_coords["y"], clicks=2)

        print("Puzzle solved!")


if __name__ == "__main__":
    main()
