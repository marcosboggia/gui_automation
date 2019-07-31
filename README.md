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

It searches windows 10 key image in the screen with at least a 80% of coincidence. If it is found it gets clicked (briefly, it opens windows 10 start menu).


* Brief explaination of GuiAuto class:
```python
Parameters
----------
tpl : image/numpy matrix with pixels.
    The image to be found.
similarity_threshold:
    It goes from 0 (no match at all) to 1 (perfect match).

Optional parameters
----------
method: OpenCV TM methods: TM_SQDIFF_NORMED, TM_CCOEFF_NORMED, TM_CCORR_NORMED
    OpenCV template match method to use. Default is TM_SQDIFF_NORMED.
thresh:
    Apply a binary threshold to images before detection. Default is False.
multiscaled:
    Applies template match multiple times with different scales of the screen.

Detects and image withing the screen and performs an action.

Methods
----------
update(): 
used to replace image to be found, similarity threshold and other parameters.

detect(): 
returns True if it finds the tpl in the image.

detect_and_move(): 
same as detect but it moves the cursor to the center of the found image withing the screen.

detect_and_click(clicks): 
Clicks the left buttons the quantity specified in clicks parameter(default 1) in the center of the
found image.

detect_and_hold(time): 
same as detect_and_click but instead of clicking X times, it holds the click @param time seconds.

detect_and_drag(start_x_fraction, start_y_fraction, end_x_fraction, end_y_fraction): 
Drags from one point to another. For more information read this function docstring.
```

* Image loader: little module to help load images from a directory.
```
Loads all images of a folder given in param path, and  assign them to a dictionary in this way: name=>image

name would be the filename without the extension.
image would be the numpy array with the image data loaded with OpenCV.

Path: relative or absolute path where the images are. Must finish with '/'.
It returns a dictionary with the names of the images as keys, and the images themselves as values.  False if any error.
```

* Another made up example with image loader:

```python
from gui_automation import GuiAuto, load_images
from time import sleep

buttons = load_images("images/buttons/")

while GuiAuto(buttons['start'], 0.8).detect_and_click():
    pass
sleep(2)
if GuiAuto(buttons['accept'], 0.8).detect_and_click():
    print("Found accept button")
```
In this case we load all images in "images/buttons/" folder and the wait until start button is found. After that, it waits 2 seconds and then it tries to find accept button.