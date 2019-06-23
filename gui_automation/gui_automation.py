# Made by Marcos Boggia

import gui_automation.image_detection as imgd
import gui_automation.mouse as mouse


def detect(tpl, similarity_threshold, method=imgd.TM_SQDIFF_NORMED, thresh=False):
    similarity, spot = imgd.Detection(tpl).tm(method, thresh)
    if similarity > similarity_threshold:
        return similarity, spot
    return False


def detect_and_click(tpl, similarity_threshold, clicks=1, method=imgd.TM_SQDIFF_NORMED, thresh=False):
    res = detect(tpl, similarity_threshold, method, thresh)
    if res:
        (similarity, spot) = res
        mouse.click(*spot.center_position(), clicks)
        return True
    return False


def detect_and_hold(tpl, similarity_threshold, time, method=imgd.TM_SQDIFF_NORMED, thresh=False):
    res = detect(tpl, similarity_threshold, method, thresh)
    if res:
        (similarity, spot) = res
        mouse.hold_click(*spot.center_position(), time)
        return True
    return False


# Ej: detect_and_drag(tpl, 0.5, '3/4', '0/1', '7/8', '4/5')
#   3/4 of the width and 0/1 of the height for START
#  __o___o_  7/8 of the width for END
# |  S     |   S = start
# |   \    |   E = end
# |    \   |   \ = the mouse drag path
# |      E o 4/5 of the height for END
# |________|
def detect_and_drag(tpl, similarity_threshold, start_x_fraction, start_y_fraction, end_x_fraction, end_y_fraction,
                    method=imgd.TM_SQDIFF_NORMED, thresh=False):
    res = detect(tpl, similarity_threshold, method, thresh)
    if res:
        (similarity, spot) = res
        start_x, start_y = spot.custom_position(*_values_from_fraction(start_x_fraction),
                                                *_values_from_fraction(start_y_fraction))
        end_x, end_y = spot.custom_position(*_values_from_fraction(end_x_fraction),
                                            *_values_from_fraction(end_y_fraction))
        mouse.drag_click(start_x, start_y, end_x, end_y)
        return True
    return False


# Used to obtain the numbers from fractions like '3/4' etc.
def _values_from_fraction(fraction):
    return int(fraction[0]), int(fraction[2])
