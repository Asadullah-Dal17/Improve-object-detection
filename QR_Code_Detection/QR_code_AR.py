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

            cv.line(image, hull[j], hull[(j + 1) % n], WHITE, 10)

        # finding width of QR code in the image
        x, x1 = hull[0][0], hull[1][0]
        y, y1 = hull[0][1], hull[1][1]
        # coordinates = (x, y, x1, y1)
        # # print(hull)
        # pt1, pt2, pt3, pt4 = hull
        Pos = hull[3]
        # using Eucaldain distance finder function to find the width
        # euclaDistance = eucaldainDistance(x, y, x1, y1)

        # retruing the Eucaldain distance/ QR code width other words
        return hull


cap = cv.VideoCapture(1)
_, frame = cap.read()
# frame = cv.resize(frame, None, fx=0.5, fy=0.5)
old_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

lk_params = dict(winSize=(10, 10),
                 maxLevel=6,
                 criteria=(cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT, 10, 1))
old_points = np.array([[]])
print(len(old_points))
QR_Detect = False
while True:
    ret, frame = cap.read()
    if ret == False:
        break
    frame = cv.resize(frame, None, fx=0.5, fy=0.5)
    # oldGray = gray
    gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    # corners, st, err = cv.calcOpticalFlowPyrLK(oldGray, gray, )
    coord = DetectQRcode(frame)
    # print(coord)

    if coord is not None:
        pt1, pt2, pt3, pt4 = coord
        QR_Detect = True
        old_points = np.array(
            [[pt1], [pt2], [pt3], [pt4]], dtype=np.float32)
        # print(old_points)

        # x, y, x1, y1 = coord
        cv.circle(frame, pt1, 8, GREEN, 3)
        cv.circle(frame, pt2, 8, (255, 0, 0), 3)
        cv.circle(frame, pt3, 8, YELLOW, 3)
        cv.circle(frame, pt4, 8, (0, 0, 255), 3)
        maxX = (max(coord, key=lambda item: item[0]))[0]
        minX = (min(coord, key=lambda item: item[0]))[0]
        maxY = (max(coord, key=lambda item: item[1]))[1]
        minY = (min(coord, key=lambda item: item[1]))[1]
        # print(maxX, minX)
        # ROI = frame[minY:maxY, minX:maxX]
        # cv.imshow('ROI', ROI)
    # if QR_Detect == True:
        new_points, status, error = cv.calcOpticalFlowPyrLK(old_gray, gray_frame, old_points, None, **lk_params)
        # old_points = new_points.astype(int)

        # for values in new_points:

        #     px, py = values.ravel()
        #     cv.circle(frame, (px, py), 7, (255, 100, 255), 2)
        # n = len(new_points)
        # listTuples = [tuple(l[0]) for l in new_points]
        # for j in range(0, n):
        #     # print(j, "      ", (j + 1) % n, "    ", n)
        #     cv.line(frame, listTuples[j],
        #             listTuples[(j + 1) % n], (0, 0, 255), 2)
        #     # print(values)

        # cv.circle(frame, (x, y), 7, (255, 0, 255), 2)
        # cv.circle(frame, (x1, y1), 7, (255, 155, 255), 2)

        old_gray = gray_frame.copy()
        # cv.imshow("ROI", ROI)
    # print(len(old_points))
    cv.imshow('frame', frame)

    key = cv.waitKey(1)
    if key == ord('q'):
        break
cv.destroyAllWindows()
cap.release()
