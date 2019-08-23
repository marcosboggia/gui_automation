# Made by Marcos Boggia
import cv2
from gui_automation.spot import Spot
from gui_automation.detector import Detector
import numpy as np
import imutils
from typing import Tuple


SQDIFF = cv2.TM_SQDIFF_NORMED
CCOEFF = cv2.TM_CCOEFF_NORMED
CCORR = cv2.TM_CCORR_NORMED


def obtain_tm_results(img, tpl, method) -> Tuple[int, Spot]:
    """
    Function that calls matchTemplate from OpenCV, normalizes similarity values and creates the Spot instance.

    :param tpl: image/numpy matrix with pixels. The image to be found.
    :param img: image/numpy matrix with pixels. The image which will be searched.
    :param method: opencv template match method to use: SQDIFF, CCOEFF, CCORR. Default is SQDIFF
    :return: similarity, Spot
    similarity level: 0(no similarity) - 1(exact match)
    Spot instance which wraps all positions/coordinates of the found image.
    """
    result = cv2.matchTemplate(img, tpl, method)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
        similarity = abs(min_val - 1)
        position = min_loc
    else:
        similarity = max_val
        position = max_loc
    return similarity, Spot(position, tpl.shape)


class TMDetector(Detector):
    """
    Class that wraps the template match detection.
    __init__() method has two optional parameters explained in docs.
    detect() method applies matchTemplate from OpenCV and returns similarity and coordinates wrapped in 'Spot' instance.
    """

    def __init__(self, method=SQDIFF, thresh=False):
        """
        :param method: opencv template match method to use: SQDIFF, CCOEFF, CCORR. Default is SQDIFF
        :param thresh: apply threshold binary filter.
        """
        self.method = method
        self.thresh = thresh

    @staticmethod
    def _apply_binary_thresh(tpl, img):
        _, tpl = cv2.threshold(tpl, 127, 255, cv2.THRESH_BINARY)
        _, img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
        return tpl, img

    # OpenCV Template Matching

    def detect(self, tpl, img):
        """
        Applies the matchTemplate to detect 'tpl' image over 'image' image.
        :param tpl: image/numpy matrix with pixels. The image to be found.
        :param img: image/numpy matrix with pixels. The image which will be searched.
        :return: similarity, Spot
        similarity level: 0(no similarity) - 1(exact match)
        Spot instance which wraps all positions/coordinates of the found image.
        """
        tpl = cv2.cvtColor(tpl, cv2.COLOR_BGR2GRAY)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        if self.thresh:
            tpl, img = self._apply_binary_thresh(tpl, img)
        return obtain_tm_results(img, tpl, self.method)


class MultiscaledTMDetector(TMDetector):
    """ Child class of TMDetector. Same behaviour but detection occurs by resizing 'img' multiple times."""

    def __init__(self, method=SQDIFF, thresh=False, reduce_sc=0.2, magnify_sc=2.0, cant_sc=40):
        """
        :param method: opencv template match method to use: SQDIFF, CCOEFF, CCORR. Default is SQDIFF
        :param thresh: apply threshold binary filter.
        :param reduce_sc: size to downsize the image. Default is 0.2 --> 20% of the image.
        :param magnify_sc: size to upsize the image. Default is 2.0 --> 2x of the image.
        :param cant_sc: how many times the image will be resized within above values.
        """
        super().__init__(method, thresh)
        self.reduce_sc = reduce_sc
        self.magnify_sc = magnify_sc
        self.cant_sc = cant_sc

    def detect(self, tpl, img):
        """
        Applies the matchTemplate to detect 'tpl' image over 'image' image. 'image' gets resized in multiple scales.
        :param tpl: image/numpy matrix with pixels. The image to be found.
        :param img: image/numpy matrix with pixels. The image which will be searched.
        :return:
        """
        tpl = cv2.cvtColor(tpl, cv2.COLOR_BGR2GRAY)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        if self.thresh:
            tpl, img = self._apply_binary_thresh(tpl, img)
        similarity, spot = obtain_tm_results(img, tpl, self.method)

        tpl_height, tpl_width = tpl.shape[:2]
        # Iterate through scales, resizing the image/screen and find better match for tpl.
        # Reducing up to reduce_sc. Default is 0.2, meaning it will resize image to a 0.2 of its size
        # Magnifying up to magnify_sc. Default is 2.0, meaning it will enlarge the image up to a double of its size
        for scale in np.linspace(self.reduce_sc, self.magnify_sc, self.cant_sc)[::-1]:
            # Resize
            resized = imutils.resize(img, width=int(img.shape[1] * scale))
            # if the resized image is smaller than the template, then break from the loop
            if resized.shape[0] < tpl_height or resized.shape[1] < tpl_width:
                break
            # apply tm
            new_similarity, new_spot = obtain_tm_results(resized, tpl, self.method)
            # keep the best match
            if new_similarity > similarity:
                similarity = new_similarity
                # Fix resized image coordinates.
                new_spot.revert_scaled_position_error(scale)
                spot = new_spot

        return similarity, spot
