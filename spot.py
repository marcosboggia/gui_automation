# Made by Marcos Boggia


# Wraps all position/coordinates calculations for the found spot.
class Spot:

    def __init__(self, position, tpl_shape):
        self.position = position
        self.tpl_shape = tpl_shape

    # Position calculations

    def upper_left_position(self):
        return self.position

    def upper_right_position(self):
        new_y = self.position[1] + self.tpl_shape[1]
        return self.position[0], new_y

    def bottom_left_position(self):
        new_x = int(self.position[0] + self.tpl_shape[0])
        return new_x, self.position[1]

    def bottom_right_position(self):
        new_x = self.position[0] + self.tpl_shape[0]
        new_y = self.position[1] + self.tpl_shape[1]
        return new_x, new_y

    def center_position(self):
        new_x = int(self.position[0] + self.tpl_shape[0] / 2)
        new_y = int(self.position[1] + self.tpl_shape[1] / 2)
        return new_x, new_y

    # This function helps calculate any coordinate inside the image to be detected.
    # Ej: x, y = custom_position(3, 8, 1, 2)
    #   3/8 of the width
    #  __o_____
    # |        |
    # |        |
    # |  x     o 1/2 of the height
    # |        |
    # |________|
    #
    def custom_position(self, x_multiplier, x_modifier, y_multiplier, y_modifier):
        new_x = int(self.position[0] + self.tpl_shape[0] / x_modifier * x_multiplier)
        new_y = int(self.position[1] + self.tpl_shape[1] / y_modifier * y_multiplier)
        return new_x, new_y
