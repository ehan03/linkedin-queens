# standard library imports
import sys

sys.path.append(".")

# third party imports
import cv2 as cv
import numpy as np
import pyautogui
from mss import mss

# local imports
from src import GridExtractor, LinkedInQueensSolver
from src.constants import WINDOW_HEIGHT, WINDOW_WIDTH


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
        print(
            "Black pixels found in cell centers. Did you already solve the puzzle? Exiting..."
        )
    else:
        solver = LinkedInQueensSolver(colors)
        solution = solver.solve()

        for idx, row in zip(solution, centers):
            target_coords = row[idx]
            pyautogui.click(x=target_coords["x"], y=target_coords["y"], clicks=2)

        print("Puzzle solved. Go flex your inhuman speed on LinkedIn now.")


if __name__ == "__main__":
    main()
