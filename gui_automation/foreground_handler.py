# Made by Marcos Boggia
import pyautogui
from time import sleep
import numpy as np
from pyautogui import screenshot
from gui_automation.handler import Handler

pyautogui.PAUSE = 1
pyautogui.FAILSAFE = False


class ForegroundHandler(Handler):
    """ Default handler. It screenshots the viewable screen and performs clicks on it."""
    @staticmethod
    def screenshot():
        return np.array(screenshot())[:, :, ::-1].copy()

    @staticmethod
    def click(x, y, clicks=1):
        pyautogui.click(x=x, y=y, button='left', clicks=clicks, interval=0.5)

    @staticmethod
    def move(x, y):
        pyautogui.moveTo(x=x, y=y)

    @staticmethod
    def hold_click(x, y, time):
        pyautogui.PAUSE = 0
        refresh_rate = 0.05
        pyautogui.mouseDown(x=x, y=y, button='left')
        while time > 0:
            sleep(refresh_rate)
            pyautogui.moveTo(x=x, y=y)
            time -= refresh_rate

        pyautogui.mouseUp(x=x, y=y, button='left')
        pyautogui.PAUSE = 1

    @staticmethod
    def drag_click(start_x, start_y, end_x, end_y):
        pyautogui.moveTo(x=start_x, y=start_y)
        pyautogui.dragTo(x=end_x, y=end_y, button='left', duration=1)

    @staticmethod
    def press_key(key):
        pyautogui.press(key)

    @staticmethod
    def press_hotkey(*keys):
        pyautogui.hotkey(*keys)

    @staticmethod
    def write_string(key, interval):
        pyautogui.write(key, interval)

