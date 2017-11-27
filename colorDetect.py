import cv2
import numpy as np

def find_marker(image):
    edged = cv2.Canny(image, 35, 125)
    (cnts, _) = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    c = max(cnts, key=cv2.contourArea)
    return cv2.minAreaRect(c)


cam = cv2.VideoCapture(0)

while True:
    print("this")
    ret, img = cam.read()
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    lower_range = np.array([0, 154, 125])
    upper_range = np.array([13, 235, 215])

    mask = cv2.inRange(hsv, lower_range, upper_range)
    temp = cv2.GaussianBlur(mask, (5, 5), 0)

    marker = find_marker(temp)
    box = np.int0(cv2.cv.BoxPoints(marker))
    cv2.drawContours(img, [box], -1, (0, 255, 0), 2)

    cv2.imshow("image", img)

    if cv2.waitKey(1) == 27:
        break

cam.release()
cv2.destroyAllWindows()