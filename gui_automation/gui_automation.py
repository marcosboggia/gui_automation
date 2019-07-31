# Made by Marcos Boggia

import gui_automation.image_detection as imgd
import gui_automation.mouse as mouse
import functools


def _detect(func):
    """

    :param func: behaviour to inject if the detection fits the similarity threshold
    :return: decorated function
    """
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        det = imgd.Detection(self.tpl)
        if self.multiscaled:
            if self.multiscaled is True:
                self.similarity, self.spot = det.tm_multiscaled(self.method, self.thresh)
            else:
                self.similarity, self.spot = det.tm_multiscaled(self.method, self.thresh, *self.multiscaled)
        else:
            self.similarity, self.spot = det.tm(self.method, self.thresh)
        if self.similarity > self.similarity_threshold:
            func(self, *args, **kwargs)
            return True
        self.spot = None
        return False

    return wrapper


class GuiAuto:
    """
    Detects and image withing the screen and performs an action.

    Methods
    ----------
    update: used to replace image to be found, similarity threshold and other parameters.
    detect: returns True if it finds the tpl in the image.
    detect_and_move: same as detect but it moves the cursor to the center of the found image withing the screen.
    detect_and_click: Clicks the left buttons the quantity specified in @param click(default 1) in the center of the
                      found image.
    detect_and_hold: same as detect_and_click but instead of clicking X times, it holds the click @param time seconds.
    detect_and_drag: Drags from one point to another. For more information read this function docstring.

    """

    def __init__(self, tpl=None, similarity_threshold=None, method=imgd.TM_CCOEFF_NORMED, thresh=False, multiscaled=False):
        """
        Parameters
        ----------
        tpl : image/numpy matrix with pixels.
            The image to be found.
        similarity_threshold:
            It goes from 0 (no match at all) to 1 (perfect match).

        Optional parameters
        ----------
        method: OpenCV TM methods: TM_SQDIFF_NORMED, TM_CCOEFF_NORMED, TM_CCORR_NORMED
            OpenCV template match method to use. Default is TM_SQDIFF_NORMED.
        thresh:
            Apply a binary threshold to images before detection. Default is False.
        multiscaled:
            Applies template match multiple times with different scales of the screen.
        """
        self.tpl = tpl
        self.similarity_threshold = similarity_threshold
        self.method = method
        self.thresh = thresh
        self.multiscaled = multiscaled
        self.similarity = None
        self.spot = None

    def update(self, tpl, similarity_threshold, method=imgd.TM_CCOEFF_NORMED, thresh=False, multiscaled=False):
        """
        Same parameters as class instantiation. Used to update image to be found and the similarity threshold (instead
        of creating a new instance with these new values) and other parameters optionally.
        """
        self.tpl = tpl
        self.similarity_threshold = similarity_threshold
        self.method = method
        self.thresh = thresh
        self.multiscaled = multiscaled
        return self

    @_detect
    def detect(self):
        pass

    @_detect
    def detect_and_move(self):
        mouse.move(*self.spot.center_position())

    @_detect
    def detect_and_click(self, clicks=1):
        mouse.click(*self.spot.center_position(), clicks)

    @_detect
    def detect_and_hold(self, time):
        mouse.hold_click(*self.spot.center_position(), time)

    @_detect
    def detect_and_drag(self, start_x_fraction, start_y_fraction, end_x_fraction, end_y_fraction):
        """
        @brief Drags the mouse from one point to another using the tpl width and height to calculate starting and ending
                points. All params are fractions in the following string format: 'number/number'.
        @example GuiAuto(img, 0.8).detect_and_drag('3/4', '0/1', '7/8', '4/5')

           3/4 of the width and 0/1 of the height for START
          __o___o_  7/8 of the width for END
         |  S     |   S = start
         |   \\    |   E = end
         |    \\   |   \\ = the mouse drag path
         |      E o 4/5 of the height for END
         |________|
        """
        start_x, start_y = self.spot.custom_position(*_values_from_fraction(start_x_fraction),
                                                     *_values_from_fraction(start_y_fraction))
        end_x, end_y = self.spot.custom_position(*_values_from_fraction(end_x_fraction),
                                                 *_values_from_fraction(end_y_fraction))
        mouse.drag_click(start_x, start_y, end_x, end_y)


# Used to obtain the numbers from fractions like '3/4' etc.
def _values_from_fraction(fraction):
    return int(fraction[0]), int(fraction[2])
