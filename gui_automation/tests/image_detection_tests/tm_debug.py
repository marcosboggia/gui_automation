# Made by Marcos Boggia

from image_detection import Detection
import cv2

random = cv2.imread("../images/tpl/random.png")
blank = cv2.imread("../images/tpl/blank.png")
black = cv2.imread("../images/tpl/black.png")
win10key = cv2.imread("../images/tpl/win10key.png")
screen = cv2.imread("../images/screens/screen_changed.png")

bad_det = Detection(random, screen)
good_det = Detection(win10key, screen)

similarity, spot = bad_det.tm_sqdiff_normed(thresh=True)
similarity2, spot2 = good_det.tm_sqdiff_normed(thresh=True)
print(f'SQDIFF_NORMED:')
print(f'bad   : {similarity}')
print(f'good  : {similarity2}\n')

similarity, spot = bad_det.tm_ccoeff_normed(thresh=True)
similarity2, spot2 = good_det.tm_ccoeff_normed(thresh=True)
print(f'CCOEFF_NORMED:')
print(f'bad   : {similarity}')
print(f'good  : {similarity2}\n')

similarity, spot = bad_det.tm_ccorr_normed(thresh=True)
similarity2, spot2 = good_det.tm_ccorr_normed(thresh=True)
print(f'CORR_NORMED:')
print(f'bad   : {similarity}')
print(f'good  : {similarity2}\n')


similarity, spot = bad_det.tm_sqdiff_normed()
similarity2, spot2 = good_det.tm_sqdiff_normed()
print(f'SQDIFF_NORMED:')
print(f'bad   : {similarity}')
print(f'good  : {similarity2}\n')

similarity, spot = bad_det.tm_ccoeff_normed()
similarity2, spot2 = good_det.tm_ccoeff_normed()
print(f'CCOEFF_NORMED:')
print(f'bad   : {similarity}')
print(f'good  : {similarity2}\n')

similarity, spot = bad_det.tm_ccorr_normed()
similarity2, spot2 = good_det.tm_ccorr_normed()
print(f'CORR_NORMED:')
print(f'bad   : {similarity}')
print(f'good  : {similarity2}\n')

while True:
    frame = screen.copy()

    cv2.circle(frame, spot.default_position(), 2, (0, 255, 0), 2)
    cv2.circle(frame, spot.bottom_right_position(), 2, (0, 255, 0), 2)
    cv2.circle(frame, spot.center_position(), 5, (0, 0, 255), 3)
    cv2.putText(frame, str(round(similarity, 3)), spot.position, cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 1)

    cv2.circle(frame, spot2.default_position(), 2, (0, 255, 0), 2)
    cv2.circle(frame, spot2.bottom_right_position(), 2, (0, 255, 0), 2)
    cv2.circle(frame, spot2.center_position(), 5, (0, 0, 255), 3)
    cv2.putText(frame, str(round(similarity2, 3)), spot2.position, cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 1)

    frame = cv2.resize(frame, (int(1920 / 1.7), int(1080 / 1.7)))
    cv2.imshow("Debug", frame)
    cv2.waitKey(5)

