# Made by Marcos Boggia

import cv2
from spot import Spot
import numpy as np
from pyautogui import screenshot


TM_SQDIFF_NORMED = cv2.TM_SQDIFF_NORMED
TM_CCOEFF_NORMED = cv2.TM_CCOEFF_NORMED
TM_CCORR_NORMED = cv2.TM_CCORR_NORMED


class Detection:

    def __init__(self, tpl, img=None):
        self.tpl = tpl
        if img is None:
            self.img = np.array(screenshot())[:, :, ::-1].copy()
        else:
            self.img = img

    # OpenCV Template Matching

    def tm(self, method, thresh):

        # Create a copy of the images to be used
        img = self.img.copy()
        tpl = self.tpl.copy()

        if thresh:
            _, img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
            _, tpl = cv2.threshold(tpl, 127, 255, cv2.THRESH_BINARY)

        # Apply template Matching with the method
        res = cv2.matchTemplate(img, tpl, method)

        # Grab the Max and Min values, plus their locations
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

        if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
            similarity = abs(min_val - 1)
            position = min_loc
        else:
            similarity = max_val
            position = max_loc

        # Create spot wrapper
        spot = Spot(position, tpl.shape)

        return similarity, spot
