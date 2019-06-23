# uncompyle6 version 3.3.3
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.3 (default, Mar 27 2019, 17:13:21) [MSC v.1915 64 bit (AMD64)]
# Embedded file name: C:\Users\marcos.boggia\PythonProjects\gui-automation\gui_auto_wrapper.py
# Size of source mod 2**32: 4453 bytes
from time import sleep
import pyautogui, numpy as np
from cv2.cv2 import cv2
from save_screenshots import save_screenshot
width, height = pyautogui.size()
screen = np.zeros([100, 100, 3], dtype=(np.uint8))

def print_similarity(value):
    print(('\r%3.3f' % value), end='')


def configure_pyautogui(pause=1, failsafe=False):
    pyautogui.PAUSE = pause
    pyautogui.FAILSAFE = failsafe


def take_screenshot():
    global screen
    screen = np.array(pyautogui.screenshot())[:, :, ::-1].copy()


def hold_click(x, y, time):
    pyautogui.PAUSE = 0
    refresh_rate = 0.05
    pyautogui.mouseDown(x=x, y=y)
    while 1:
        if time > 0:
            pyautogui.moveTo(x=x, y=y)
            sleep(refresh_rate)
            time -= refresh_rate

    pyautogui.mouseUp()
    pyautogui.PAUSE = 1


def detection(img):
    take_screenshot()
    result = cv2.matchTemplate(img, screen, cv2.TM_SQDIFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    print_similarity(min_val)
    return (
     min_val, max_val, min_loc, max_loc)


def threshold_detection(img):
    take_screenshot()
    _, screen_thresh = cv2.threshold(screen, 127, 255, cv2.THRESH_BINARY)
    _, img_thresh = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
    result = cv2.matchTemplate(img_thresh, screen_thresh, cv2.TM_SQDIFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    print_similarity(min_val)
    return (
     min_val, max_val, min_loc, max_loc)


def detect(img, similarity, thing_msg, detection_mode=detection):
    img = img[0]
    min_val, max_val, min_loc, max_loc = detection_mode(img)
    if min_val < similarity:
        print('\nFound ' + thing_msg)
        return True
    else:
        return False


def detect_and_click(img, similarity, thing_msg, mod_coords=None, d_click=False, hold_time=0, detection_mode=detection):
    img = img[0]
    min_val, max_val, coordinates, max_loc = detection_mode(img)
    if min_val < similarity:
        print('\nFound ' + thing_msg)
        if mod_coords is not None:
            coordinates = mod_coords(coordinates, img)
        if d_click:
            (pyautogui.click)(*coordinates)
            sleep(0.5)
            (pyautogui.click)(*coordinates)
            sleep(0.5)
            (pyautogui.click)(*coordinates)
        else:
            if hold_time != 0:
                hold_click(*coordinates, *(hold_time,))
            else:
                (pyautogui.click)(*coordinates)
        if thing_msg == 'DEBUG':
            while True:
                cv2.imshow('f', img[0])
                cv2.waitKey(5)

        return True
    else:
        return False


def detect_and_move(img, similarity, thing_msg, detection_mode=detection):
    img = img[0]
    min_val, max_val, coordinates, max_loc = detection_mode(img)
    if min_val < similarity:
        print('\nFound ' + thing_msg)
        (pyautogui.moveTo)(*coordinates)
        return True
    else:
        return False


def detect_and_drag(img, similarity, thing_msg, modify_coords, detection_mode=detection, **kwargs):
    img = img[0]
    min_val, max_val, start, max_loc = detection_mode(img)
    if min_val < similarity:
        print('\nFound ' + thing_msg)
        start, end = modify_coords(start, img, **kwargs)
        (pyautogui.moveTo)(*start)
        (pyautogui.dragTo)(*end, **{'duration': 1})
        return True
    else:
        return False


def detect_and_click_multiple(imgs, similarity, thing_msg, mod_coords=None, detection_mode=detection, d_click=False):
    for img in imgs:
        if detect_and_click(img, similarity, thing_msg, mod_coords=mod_coords, detection_mode=detection_mode, d_click=d_click):
            return (True, img)

    return False


def detect_multiple(imgs, similarity, thing_msg, detection_mode=detection):
    for img in imgs:
        if detect(img, similarity, thing_msg, detection_mode=detection_mode):
            return (True, img)

    return False


def save_last_screen(name):
    save_screenshot('tmp', name, screen)
# okay decompiling .\gui_auto_wrapper.cpython-37.pyc
