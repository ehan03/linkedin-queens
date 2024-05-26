# standard library imports
import os
import sys

os.system("")
sys.path.append(".")

# third party imports
import cv2 as cv
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

    start_template = cv.imread("img/template_start.png", cv.IMREAD_UNCHANGED)
    extractor = GridExtractor()
    monitor = {
        "top": 0,
        "left": 0,
        "width": WINDOW_WIDTH,
        "height": WINDOW_HEIGHT,
    }

    with mss() as sct:
        while True:
            start_image = sct.grab(monitor)
            start_image = np.array(start_image)
            result = cv.matchTemplate(start_image, start_template, cv.TM_CCOEFF_NORMED)
            _, maxVal, _, maxLoc = cv.minMaxLoc(result)

            if maxVal > 0.99:
                print("Found 'Start game' button.\n")
                start_button_x = maxLoc[0] + start_template.shape[1] // 2
                start_button_y = maxLoc[1] + start_template.shape[0] // 2
                pyautogui.click(x=start_button_x, y=start_button_y)
                break

        while True:
            pyautogui.hotkey("ctrl", "home")
            game_image = sct.grab(monitor)
            game_image = np.array(game_image)
            is_present = extractor.check_template(game_image)

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
