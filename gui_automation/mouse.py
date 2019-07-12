# Made by Marcos Boggia
# Official Doc: https://pyautogui.readthedocs.io/en/latest/mouse.html

import pyautogui
from time import sleep

pyautogui.PAUSE = 1
pyautogui.FAILSAFE = False


def click(x, y, clicks=1):
    pyautogui.click(x=x, y=y, button='left', clicks=clicks, interval=0.5)


def move(x, y):
    pyautogui.moveTo(x=x, y=y)


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


def drag_click(start_x, start_y, end_x, end_y):
    pyautogui.moveTo(x=start_x, y=start_y)
    pyautogui.dragTo(x=end_x, y=end_y, button='left', duration=1)
