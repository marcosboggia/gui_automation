# Made by Marcos Boggia


class Spot:
    """
    Wraps all position/coordinates calculations for the found image.

    Available methods:
    upper_left_position()
    upper_right_position()
    bottom_left_position()
    bottom_right_position()
    center_position()
    custom_position(x_multiplier, x_modifier, y_multiplier, y_modifier)
    """
    def __init__(self, position, tpl_shape):
        """

        :param position: tuple with x and y coordinates
        :param tpl_shape: tuple with height and width of the shape
        """
        self.x = position[0]
        self.y = position[1]
        self.tpl_width = tpl_shape[1]
        self.tpl_height = tpl_shape[0]

    # Position calculations

    def upper_left(self):
        return self.x, self.y

    def upper_right(self):
        new_y = self.y + self.tpl_height
        return self.x, new_y

    def bottom_left(self):
        new_x = int(self.x + self.tpl_width)
        return new_x, self.y

    def bottom_right(self):
        new_x = self.x + self.tpl_width
        new_y = self.y + self.tpl_height
        return new_x, new_y

    def center(self):
        new_x = int(self.x + self.tpl_width / 2)
        new_y = int(self.y + self.tpl_height / 2)
        return new_x, new_y

    def custom_position(self, x_multiplier, x_modifier, y_multiplier, y_modifier):
        """
        This method helps calculate any coordinate within the image detected.
        Ej: x, y = custom_position(3, 8, 1, 2)
           3/8 of the width
          __o_____
         |        |
         |        |
         |  x     o 1/2 of the height
         |        |
         |________|

        :param x_multiplier: how many parts of the divided width to take
        :param x_modifier: in how many parts the width is going to be divided
        :param y_multiplier: same as width but with height
        :param y_modifier: same as width but with height
        :return:
        new_x, new_y: the calculated coordinates
        """
        new_x = int(self.x + self.tpl_width / x_modifier * x_multiplier)
        new_y = int(self.y + self.tpl_height / y_modifier * y_multiplier)
        return new_x, new_y

    def revert_scaled_position_error(self, scale):
        """
        If image has been resized this function must be used to fix the displacement of the position to the original
        image.
        :param scale: the scale used to resize the image
        :return: No return
        """
        self.x = int(self.x/scale)
        self.y = int(self.y/scale)
