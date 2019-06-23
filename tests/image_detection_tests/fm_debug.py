# Made by Marcos Boggia

from image_detection import Detection
import cv2

random = cv2.imread("../images/tpl/random.png")
win10key = cv2.imread("../images/tpl/win10key200.png")
screen = cv2.imread("../images/screens/screen.png")

bad_det = Detection(random, screen)
good_det = Detection(win10key, screen)

debug = good_det.fm_brute_force()

while True:
    frame = screen.copy()



    frame = cv2.resize(frame, (int(1920 / 1.7), int(1080 / 1.7)))
    cv2.imshow("Debug", frame)
    cv2.waitKey(5)
