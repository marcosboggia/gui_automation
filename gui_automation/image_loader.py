import cv2
import os


def load_images(path):
    """
    Loads all images of a folder given in param path, and  assign them to a dictionary in this way: name=>image

    name would be the filename without the extension.
    image would be the numpy array with the image data loaded with OpenCV.

    :param path: path where the images are. Must finish with '/'
    :return: dictionary with the names of the images as keys, and the images themselves as values.  False if any error
    """
    if not path[-1] == '/':
        return False
    images = {}
    try:
        dirs = os.listdir(path)
    except FileNotFoundError:
        return False
    for name in dirs:
        img = cv2.imread(path + name)
        if img is None:
            return False
        name = name.split('.')[0]
        images[name] = img
    return images
