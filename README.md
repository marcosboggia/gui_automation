# Gui automation

Simple python library useful for automating tasks using images.

It uses OpenCV and PyAutoGui. Made for Python 3.7+.

* Little example: 

```python
import cv2
import gui_automation as ga

tpl = cv2.imread("tests/images/tpl/win10key.png")
ga.detect_and_click(tpl, 0.8)
```

It searches windows 10 key image in the screen with a 80% of coincidence at least. If it is found it gets clicked (opens windows 10 start menu).