# Gui automation

Simple python library useful for automating tasks using images.

It uses OpenCV and PyAutoGui. Made with Python 3.7.

* Little example: 

```python
import cv2
from gui_automation import GuiAuto

tpl = cv2.imread("win10key.png")
GuiAuto(tpl, 0.8).detect_and_click()
```

It searches windows 10 key image in the screen with at least a 80% of coincidence. If it is found it gets clicked (opens windows 10 start menu).


* Brief show of available methods:
```python
detect()

detect_and_move()

detect_and_click(clicks)

detect_and_hold(time)

detect_and_drag(start_x_fraction, start_y_fraction, end_x_fraction, end_y_fraction)
```