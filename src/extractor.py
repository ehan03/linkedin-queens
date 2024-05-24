# standard library imports
import math
import os
from typing import List, Tuple

# third party imports
import cv2 as cv
import numpy as np
from imutils import contours

# local imports
from .constants import MATCH_THRESHOLD, MAX_CONTOUR_AREA, MIN_CONTOUR_AREA


class GridExtractor:
    """
    Class to detect and extract the game board from a screenshot
    """

    def __init__(
        self,
        template_path: str = os.path.join(
            os.path.dirname(__file__), "..", "img", "template.png"
        ),
    ) -> None:
        """
        Initialize the GridExtractor object
        """

        self.template = cv.imread(template_path, cv.IMREAD_UNCHANGED)
        self.template_height, self.template_width = self.template.shape[:2]
        self.alpha_channel = np.array(cv.split(self.template)[3])
        self.cropped, self.cropped_x, self.cropped_y = None, None, None

    def check_template(self, image: cv.typing.MatLike) -> bool:
        """
        Check if the template is present in the image
        """

        result = cv.matchTemplate(
            image, self.template, cv.TM_SQDIFF_NORMED, mask=self.alpha_channel
        )
        minVal, _, minLoc, _ = cv.minMaxLoc(result)
        is_present = minVal < MATCH_THRESHOLD

        if is_present:
            self.cropped_x, self.cropped_y = minLoc
            self.cropped = image[
                self.cropped_y : self.cropped_y + self.template_height,
                self.cropped_x : self.cropped_x + self.template_width,
            ]

        return is_present

    def __get_grid_contours(self) -> List[np.ndarray]:
        """
        Get the contours of the grid, isolating the cells
        """

        assert self.cropped is not None
        cropped_gray = cv.cvtColor(self.cropped, cv.COLOR_BGR2GRAY)
        cropped_gray_blur = cv.GaussianBlur(cropped_gray, (5, 5), 0)
        _, thresh = cv.threshold(cropped_gray_blur, 150, 255, cv.THRESH_BINARY)

        cts = cv.findContours(thresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        cts = cts[0] if len(cts) == 2 else cts[1]
        cts = [
            c for c in cts if MIN_CONTOUR_AREA < cv.contourArea(c) < MAX_CONTOUR_AREA
        ]

        N = math.isqrt(len(cts))
        assert N * N == len(cts), "Grid is not square"

        cts, _ = contours.sort_contours(cts, method="top-to-bottom")

        grid = []
        row = []
        for i, c in enumerate(cts, 1):
            row.append(c)
            if i % N == 0:
                row, _ = contours.sort_contours(row, method="left-to-right")
                grid.append(row)
                row = []

        return grid

    def extract_grid(self, top_offset: int, left_offset: int) -> Tuple[List, List]:
        """
        Extract the grid from the screenshot
        """

        assert self.cropped is not None
        assert self.cropped_x is not None
        assert self.cropped_y is not None

        grid = self.__get_grid_contours()
        N = len(grid)
        colors = []
        centers = []

        for row in grid:
            for c in row:
                M = cv.moments(c)
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                centers.append(
                    {
                        "x": cX + left_offset + self.cropped_x,
                        "y": cY + top_offset + self.cropped_y,
                    }
                )

                b, g, r, _ = self.cropped[cY, cX]
                rgb = f"{r},{g},{b}"

                if rgb == "0,0,0":
                    return [], []

                colors.append(rgb)

        colors = np.array(colors).reshape(N, N).tolist()
        centers = np.array(centers).reshape(N, N).tolist()

        return colors, centers
