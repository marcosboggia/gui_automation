# Made by Marcos Boggia

import cv2
from gui_automation.spot import Spot
import numpy as np
from pyautogui import screenshot
import imutils


TM_SQDIFF_NORMED = cv2.TM_SQDIFF_NORMED
TM_CCOEFF_NORMED = cv2.TM_CCOEFF_NORMED
TM_CCORR_NORMED = cv2.TM_CCORR_NORMED


def obtain_tm_results(img, tpl, method):
    result = cv2.matchTemplate(img, tpl, method)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
        similarity = abs(min_val - 1)
        position = min_loc
    else:
        similarity = max_val
        position = max_loc
    return similarity, Spot(position, tpl.shape)


class Detection:

    def __init__(self, tpl, img=None):
        self.tpl = cv2.cvtColor(tpl, cv2.COLOR_BGR2GRAY)
        if img is None:
            self.img = cv2.cvtColor(np.array(screenshot())[:, :, ::-1].copy(), cv2.COLOR_BGR2GRAY)
        else:
            self.img = img

    def _apply_binary_thresh(self):
        _, img = cv2.threshold(self.img, 127, 255, cv2.THRESH_BINARY)
        _, tpl = cv2.threshold(self.tpl, 127, 255, cv2.THRESH_BINARY)
        return img, tpl

    # OpenCV Template Matching

    def tm(self, method=cv2.TM_SQDIFF_NORMED, thresh=False):
        if thresh:
            img, tpl = self._apply_binary_thresh()
        else:
            img, tpl = self.img, self.tpl
        return obtain_tm_results(img, tpl, method)

    def tm_multiscaled(self, method=cv2.TM_SQDIFF_NORMED, thresh=False, reduce_sc=0.2, magnify_sc=2.0, cant_sc=40):
        if thresh:
            img, tpl = self._apply_binary_thresh()
        else:
            img, tpl = self.img, self.tpl
        similarity, spot = obtain_tm_results(img, tpl, method)

        tpl_height, tpl_width = tpl.shape[:2]
        # Iterate through scales, resizing the image/screen and find better match for tpl.
        # Reducing up to reduce_sc. Defualt is 0.2, meaning it will resize image to a 0.2 of its size
        # Magnifying up to magnify_sc. Defualt is 2.0, meaning it will enlarge the image up to a double of its size
        for scale in np.linspace(reduce_sc, magnify_sc, cant_sc)[::-1]:
            # Resize
            resized = imutils.resize(img, width=int(img.shape[1] * scale))
            # if the resized image is smaller than the template, then break from the loop
            if resized.shape[0] < tpl_height or resized.shape[1] < tpl_width:
                break
            # apply tm
            new_similarity, new_spot = obtain_tm_results(resized, tpl, method)
            # keep the best match
            if new_similarity > similarity:
                similarity = new_similarity
                # Fix resized image coordinates.
                new_spot.revert_scaled_position_error(scale)
                spot = new_spot

        return similarity, spot
