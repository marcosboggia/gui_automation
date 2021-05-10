# Made by Marcos Boggia
from gui_automation.foreground_handler import ForegroundHandler
from gui_automation.image_detector import TMDetector


def _values_from_fraction(fraction):
    """ Used to obtain the numbers from fractions like '3/4' etc. """
    return int(fraction[0]), int(fraction[2])


class GuiAuto:
    """
    Detects and image withing the screen and performs an action.

    Methods
    ----------
    detect(tpl, img=None):
        returns Spot instance if it finds the tpl in the image. Internally, it keeps the last spot found.
    move(coords=None):
        same as detect but it moves the cursor to the center of the found image withing the screen.
    click(coords=None):
        Clicks the left buttons the quantity specified in @param click(default 1) in the center of the found image.
    hold(coords=None):
        Same as click but instead of clicking X times, it holds the click @param time seconds.
    drag(start_coords, end_coords):
        Drags from one point to another using start and end coordinates.
    drag_within(start_x_fraction, start_y_fraction, end_x_fraction, end_y_fraction):
        Drags from one point to another inside the bounding box of the image found.
    For more information read this function documentation.

    For move, click, and hold if no coords are given it performs the action on the last spot found.
    """

    def __init__(self, detector=TMDetector(), handler=ForegroundHandler()):
        """
        Wraps detection and controlling of the GUI.
        By default it will use normal detection and foreground app automation.
        :param detector: detector instance. Default is TMDetector()
        :param handler:  handler instance. Default is ForegroundHandler()
        """
        self.detector = detector
        self.handler = handler
        self.similarity = None
        self.spot = None

    def detect(self, tpl, similarity_threshold, img=None):
        """
        :param tpl: image/numpy matrix with pixels. The image to be found.
        :param similarity_threshold: it goes from 0 (no match at all) to 1 (perfect match).
        :param img: image where the tpl must be searched.
        :return:
        """
        if img is None:
            img = self.handler.screenshot()
        if img.shape[0] < tpl.shape[0] or img.shape[1] < tpl.shape[1]:
            return False
        self.similarity, self.spot = self.detector.detect(tpl, img)
        if self.similarity > similarity_threshold:
            return self.spot
        self.spot = None
        return False

    def move(self, coords=None):
        """
        :param coords: tuple in the form of (x, y) indicating coordinates to perform action.
        :return:
        """
        if coords is None:
            self.handler.move(*self.spot.center())
        else:
            self.handler.move(*coords)

    def click(self, clicks=1, coords=None):
        """
        :param coords: tuple in the form of (x, y) indicating coordinates to perform action.
        :param clicks: how many clicks to perform. Default is 1.
        :return:
        """
        if coords is None:
            self.handler.click(*self.spot.center(), clicks)
        else:
            self.handler.click(*coords, clicks)

    def hold(self, time, coords=None):
        """
        :param coords: tuple in the form of (x, y) indicating coordinates to perform action.
        :param time: how much time to hold in seconds.
        :return:
        """
        if coords is None:
            self.handler.hold_click(*self.spot.center(), time)
        else:
            self.handler.hold_click(*coords, time)

    def drag(self, start_coord, end_coord):
        """

        :param start_coord: tuple in the form of (x, y) indicating start coordinates to perform dragging.
        :param end_coord: tuple in the form of (x, y) indicating end coordinates to end dragging.
        :return:
        """
        self.handler.drag_click(*start_coord, *end_coord)

    def drag_within(self, start_x_fraction, start_y_fraction, end_x_fraction, end_y_fraction):
        """
        @brief Drags the mouse from one point to another using the tpl width and height to calculate starting and ending
                points. All params are fractions in the following string format: 'number/number'.
        @example ga.drag_within('3/4', '0/1', '7/8', '4/5')

           3/4 of the width and 0/1 of the height for START
          __o___o_  7/8 of the width for END
         |  S     |   S = start
         |   \\   |   E = end
         |    \\  |   \\ = the mouse drag path
         |      E o 4/5 of the height for END
         |________|
        """
        start_x, start_y = self.spot.custom_position(*_values_from_fraction(start_x_fraction),
                                                     *_values_from_fraction(start_y_fraction))
        end_x, end_y = self.spot.custom_position(*_values_from_fraction(end_x_fraction),
                                                 *_values_from_fraction(end_y_fraction))
        self.handler.drag_click(start_x, start_y, end_x, end_y)

    def press_key(self, key):
        self.handler.press_key(key)

    def press_hotkey(self, *keys):
        self.handler.press_hotkey(*keys)

    def write_string(self, key, interval=0.0):
        self.handler.write_string(key, interval)
