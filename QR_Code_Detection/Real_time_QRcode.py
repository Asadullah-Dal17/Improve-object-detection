import cv2 as cv
from numpy import numarray
import numpy as np
from pyzbar.pyzbar import decode
import pyzbar

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
MAGENTA = (255, 0, 255)
GREEN = (0, 255, 0)
CYAN = (255, 255, 0)
GOLD = (0, 255, 215)
YELLOW = (0, 255, 255)
ORANGE = (0, 165, 230)
point = ()
old_points = np.array([[]])


def DetectQRcode(image):
    codeWidth = 0
    x, y = 0, 0
    euclaDistance = 0
    global Pos
    # convert the color image to gray scale image
    Gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

    # create QR code object
    objectQRcode = pyzbar.pyzbar.decode(Gray)
    for obDecoded in objectQRcode:

        points = obDecoded.polygon
        # print(type(points))
        if len(points) > 4:
            hull = cv.convexHull(
                np.array([points for point in points], dtype=np.float32))
            hull = list(map(tuple, np.squeeze(hull)))
        else:
            hull = points

        n = len(hull)
        # draw the lines on the QR code
        for j in range(0, n):
            # print(j, "      ", (j + 1) % n, "    ", n)

            cv.line(image, hull[j], hull[(j + 1) % n], WHITE, 3)

        # finding width of QR code in the image
        x, x1 = hull[0][0], hull[1][0]
        y, y1 = hull[0][1], hull[1][1]
        # coordinates = (x, y, x1, y1)
        # # print(hull)
        # pt1, pt2, pt3, pt4 = hull
        Pos = hull[3]
        return hull
cap = cv.VideoCapture(1)
QR_Detect = False
while True:
    ret, frame = cap.read()
    if ret == False:
        break
    # frame = cv.resize(frame, None, fx=0.5, fy=0.5)
    # oldGray = gray
    gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    coord = DetectQRcode(frame)

    if coord is not None:
        pt1, pt2, pt3, pt4 = coord
        QR_Detect = True
        old_points = np.array(
            [[pt1], [pt2], [pt3], [pt4]], dtype=np.float32)
        # print(old_points)

        # x, y, x1, y1 = coord
        cv.circle(frame, pt1, 3, GREEN, 3)
        cv.circle(frame, pt2, 3, (255, 0, 0), 3)
        cv.circle(frame, pt3, 3, YELLOW, 3)
        cv.circle(frame, pt4, 3, (0, 0, 255), 3)
        # maxX = (max(coord, key=lambda item: item[0]))[0]
        # minX = (min(coord, key=lambda item: item[0]))[0]
        # maxY = (max(coord, key=lambda item: item[1]))[1]
        # minY = (min(coord, key=lambda item: item[1]))[1]

    cv.imshow('frame', frame)

    key = cv.waitKey(1)
    if key == ord('q'):
        break
cv.destroyAllWindows()
cap.release()
