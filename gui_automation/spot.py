# Made by Marcos Boggia


# Wraps all position/coordinates calculations for the found spot.
class Spot:
    """
    Spot class, wraps the position of a the found image.

    Available methods:
    upper_left_position()
    upper_right_position()
    bottom_left_position()
    bottom_right_position()
    center_position()
    custom_position(x_multiplier, x_modifier, y_multiplier, y_modifier)

    """
    def __init__(self, position, tpl_shape):
        self.position = position
        self.tpl_shape = tpl_shape

    # Position calculations

    def upper_left_position(self):
        return self.position

    def upper_right_position(self):
        new_y = self.position[1] + self.tpl_shape[0]
        return self.position[0], new_y

    def bottom_left_position(self):
        new_x = int(self.position[0] + self.tpl_shape[1])
        return new_x, self.position[1]

    def bottom_right_position(self):
        new_x = self.position[0] + self.tpl_shape[1]
        new_y = self.position[1] + self.tpl_shape[0]
        return new_x, new_y

    def center_position(self):
        new_x = int(self.position[0] + self.tpl_shape[1] / 2)
        new_y = int(self.position[1] + self.tpl_shape[0] / 2)
        return new_x, new_y

    def custom_position(self, x_multiplier, x_modifier, y_multiplier, y_modifier):
        """
        This function helps calculate any coordinate inside the image to be detected.
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
        new_x = int(self.position[0] + self.tpl_shape[1] / x_modifier * x_multiplier)
        new_y = int(self.position[1] + self.tpl_shape[0] / y_modifier * y_multiplier)
        return new_x, new_y

    def revert_scaled_position_error(self, scale):
        """
        If image has been resized this function must be used to fix the displacement of the position to the original
        image.
        :param scale: the scale used to resize the image
        :return: No return
        """
        x = self.position[0]
        y = self.position[1]
        self.position = (int(x/scale), int(y/scale))
