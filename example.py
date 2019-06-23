import cv2
from gui_automation import detect_and_click

tpl = cv2.imread("tests/images/tpl/win10key.png")
detect_and_click(tpl, 0.8)
