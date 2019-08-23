# Gui automation

Simple python library useful for automating tasks using images. It can run on Windows background applications.

It uses OpenCV and PyAutoGui. Made with Python 3.7.

#### Simple example: 

```python
import cv2
from gui_automation import GuiAuto

image_path = "win10key.png"
ga = GuiAuto()
if ga.detect(cv2.imread(image_path), 0.8):
    ga.click()
```

It searches windows 10 key image in the screen with at least a 80% of coincidence. If it is found it gets clicked (it opens windows 10 start menu).


##### The core class is GuiAuto:
Wraps detection and controlling of the GUI.
By default it will use normal image detection and foreground app automation.

* Parameters
```
detector: detector instance. Default is TMDetector()
handler:  handler instance. Default is ForegroundHandler()
```
* Methods
```
detect: returns Spot instance if it finds the tpl in the image.
move: it moves the cursor to given coordinates or the center of the found image withing the screen.
click: Clicks the left buttons the quantity specified in parameter click(default 1) in given coordinates or the center.
hold: same as click but instead of clicking X times, it holds the click a given quantity of seconds received in time parameter.
drag: Drags from one point to another. For more information read this function documentation.
```
##### Detector:
Searches an image inside another image using template match from OpenCV.
Classes with default parameters:
```
TMDetector(method=SQDIFF, thresh=False)
Applies the normal detection.

MultiscaledTMDetector(method=SQDIFF, thresh=False, reduce_sc=0.2, magnify_sc=2.0, cant_sc=40)
Applies detection multiples times while resizing the image. Parameters specify how image is resized.
```
* Parameters
```
method: template method to use. Could be SQDIFF, CCOEFF or CCORR.
thresh: boolean that specifies if binary threshold filter must be used for detection.
reduce_sc: how much the image is reduced.
magnify_sc how much the image is enlarged.
cant_sc= how many resizing will be applied.
```

##### Handler:
Interacts with the app or environment to be automated. Performs clicks, drags among others; and also obtains the screen of the app/environment on an image format.
```
ForegroundHandler()
Normal handler that takes screenshot and simulates mouse action normally.

BackgroundHandlerWin32(app_name, *args)
Handler that works in not vieawable/background applications. It requires an application/window name, and it's possible to pass as arguments a names hierarchy of the UI elements of the application.
Works only for Windows.
```

##### Spot:

Wraps all position/coordinates calculations for the found image.

* Methods:
```
upper_left_position()
upper_right_position()
bottom_left_position()
bottom_right_position()
center_position()
custom_position(x_multiplier, x_modifier, y_multiplier, y_modifier)
For this last one, check its documentation to understand parameters.
```

##### Image loader:
Little module to help load images from a directory.
Loads all images of a folder given in param path, and  assign them to a dictionary in this way: name=>image
name would be the filename without the extension.
image would be the numpy array with the image data loaded with OpenCV.
Path: relative or absolute path where the images are. Must finish with '/'.
It returns a dictionary with the names of the images as keys, and the images themselves as values.
Returns False if any error.

* Eg:

```python
from gui_automation import GuiAuto, load_images
from time import sleep

buttons = load_images("images/buttons/")

ga = GuiAuto()
while not ga.detect(buttons['start'], 0.8).detect():
    ga.click()
sleep(2)
if ga.detect(buttons['accept'], 0.8):
    print("Found accept button")
```
In this case we load all images in "images/buttons/" folder and the wait until start button is found. After that, it waits 2 seconds and then it tries to find accept button.


##### Another example:
```python
image_path = "win10keyresized.PNG"
ga = GuiAuto(detector=MultiscaledTMDetector())
spot = ga.detect(cv2.imread(image_path), 0.8)
if spot:
    ga.click(coords=spot.bottom_right(), clicks=3 )
```
In this case we have a similar win10key image to our original located on our rendered screen. So using MultiscaledTMDetector fixes our problem resizing the screen multiple times. If it is detected, it clicks the bottom right of the image found three times.
