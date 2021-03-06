# import the necessary packages
import cv2 as cv 
import numpy as np
from pyzbar.pyzbar import decode
import pyzbar


# now let's initialize the list of reference point
# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
MAGENTA = (255, 0, 255)
GREEN = (0, 255, 0)
CYAN = (255, 255, 0)
GOLD = (0, 255, 215)
YELLOW = (0, 255, 255)
ORANGE = (0, 165, 230)

# QR code detector function 


def detectQRcode(image):
    # global Pos
    # convert the color image to gray scale image
    Gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

    # create QR code object
    objectQRcode = pyzbar.pyzbar.decode(Gray)
    for obDecoded in objectQRcode: 
        x, y, w, h =obDecoded.rect
        # cv.rectangle(image, (x,y), (x+w, y+h), ORANGE, 4)
        points = obDecoded.polygon
        # print(points)
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
        # Pos = hull[3]
        return hull

ref_point = []
click = False
points =()
cap = cv.VideoCapture(1)
_, frame = cap.read()
old_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

lk_params = dict(winSize=(20, 20),
                 maxLevel=4,
                 criteria=(cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT, 10, 0.01))
  
cap =cv.VideoCapture(0)
point_selected = False
points = [()]
old_points = np.array([[]])
qr_detected= False
# stop_code=False


# keep looping until the 'q' key is pressed
while True:
    ret, frame = cap.read()
    cv.imshow('old frame ', old_gray)
    gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    # display the image and wait for a keypress
    clone = frame.copy()
    hull_points =detectQRcode(frame)
    # print(old_points.size)
    stop_code=False
    if hull_points:
        cv.putText(frame, 'PyZbar', (30,50), cv.FONT_HERSHEY_COMPLEX, 1.0, YELLOW, 2)
        pt1, pt2, pt3, pt4 = hull_points
        qr_detected= False
        stop_code=True
        old_points = np.array([pt1, pt2, pt3, pt4], dtype=np.float32)

        cv.circle(frame, pt1, 3, GREEN, 3)
        cv.circle(frame, pt2, 3, (255, 0, 0), 3)
        cv.circle(frame, pt3, 3, YELLOW, 3)
        cv.circle(frame, pt4, 3, (0, 0, 255), 3)
    if qr_detected and stop_code==False:
        cv.putText(frame, 'Optical Flow', (30,50), cv.FONT_HERSHEY_COMPLEX, 1.0, YELLOW, 2)

        # print('detecting')
        new_points, status, error = cv.calcOpticalFlowPyrLK(old_gray, gray_frame, old_points, None, **lk_params)
        old_points = new_points 
        new_points=new_points.astype(int)
        n = (len(new_points))
        cv.line(frame, new_points[0], new_points[1], MAGENTA, 3)
        cv.line(frame, new_points[1], new_points[2], MAGENTA, 3)
        cv.line(frame, new_points[2], new_points[3], MAGENTA, 3)
        cv.line(frame, new_points[3], new_points[0], MAGENTA, 3)
        cv.circle(frame, (new_points[0]), 3, GREEN, 2)




        # [cv.line(frame, new_points[j], new_points[(j + 1) % n], YELLOW, 4) for j in new_points]

        # x, y = new_points.ravel()
        # print(new_points[0])


    old_gray = gray_frame.copy()
    # press 'r' to reset the window
    key = cv.waitKey(1)
    if key == ord("r"):
        frame = clone.copy()

    # if the 'c' key is pressed, break from the loop
    elif key == ord("q"):
        break
    cv.imshow("image", frame)


# close all open windows
cv.destroyAllWindows()  