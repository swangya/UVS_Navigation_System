import cv2
import numpy as np

def find_marker(image):
    edged = cv2.Canny(image, 35, 125)
    (cnts, _) = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    if cnts != []:
        c = max(cnts, key=cv2.contourArea)
        return cv2.minAreaRect(c)
    else:
        return None

def distance_to_camera(knownWidth, focalLength, perWidth):
    return (knownWidth * focalLength) / perWidth


cam = cv2.VideoCapture(0)
KNOWN_DISTANCE = 10.5
KNOWN_WIDTH = 3
focalLength = 675.634689331
width = cam.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH)
height = cam.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT)

center = [width/2, height/2]
print center

while True:
    ret, img = cam.read()
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    lower_range = np.array([0, 63, 35])
    upper_range = np.array([32, 255, 185])

    mask = cv2.inRange(hsv, lower_range, upper_range)
    temp = cv2.GaussianBlur(mask, (5, 5), 0)

    marker = find_marker(temp)
    if marker != None:
        inches = distance_to_camera(KNOWN_WIDTH, focalLength, marker[1][0])

        box = np.int0(cv2.cv.BoxPoints(marker))
        cv2.drawContours(img, [box], -1, (0, 255, 0), 2)
        cv2.putText(img, "%.2fft" % (inches / 12),
                    (img.shape[1] - 200, img.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX,
                    2.0, (0, 255, 0), 3)
        widthHalf = marker[1][0]/2
        heightHalf = marker[1][1]/2
        destCenter = [int(marker[0][0] + widthHalf), int(marker[0][1] + heightHalf)]

        horizontalDiff = center[0]-destCenter[0]
        distRemain = inches - 10
        #print horizontalDiff
        if distRemain < 0:
            print "Command: STOP"
        elif horizontalDiff > 0:
            print "Command: Left Skid Turn    Distance Remain: ", distRemain
        elif horizontalDiff < 0:
            print "Command: Right Skid Turn   Distance Remain: ", distRemain
        elif horizontalDiff == 0:
            print "Command: Forward    Distance Remain: ", distRemain
        else:
            print "Err"
    else:
        print "Destination not Found, Command: Turn Camera"
    cv2.imshow("image", img)

    if cv2.waitKey(1) == 27:
        break

cam.release()
cv2.destroyAllWindows()
