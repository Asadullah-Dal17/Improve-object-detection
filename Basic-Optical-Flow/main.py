import cv2 as cv
import numpy as np

cap = cv.VideoCapture(0)
_, frame = cap.read()
old_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

lk_params = dict(winSize=(20, 20),
                 maxLevel=4,
                 criteria=(cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT, 10, 0.01))


def selected_Point(event, x, y, flags, params):
    global point, point_selected, old_points
    if event == cv.EVENT_LBUTTONDOWN:
        point = (int(x), int(y))
        print(point)
        point_selected = True
        old_points = np.array([[x, y]], dtype=np.float32)


cv.namedWindow('frame')
cv.setMouseCallback("frame", selected_Point)

point_selected = False
point = ()
old_points = np.array([[]])

while True:
    ret, frame = cap.read()
    cv.imshow('old frame ', old_gray)
    gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    print(old_points.astype(int))
    if point_selected is True:

        cv.circle(frame, point, 5, (155, 0, 255), -1)
        new_points, status, error = cv.calcOpticalFlowPyrLK(
            old_gray, gray_frame, old_points, None, **lk_params)

        old_points = new_points
        new_points=new_points.astype(int)

        print(type(new_points))
        x, y = new_points.ravel()
        print(x, y)
        cv.circle(frame, (x, y), 6, (0, 255, 255), 4)
        # cv.cricle(frame, )
    old_gray = gray_frame.copy()
    cv.imshow('frame', frame)
    key = cv.waitKey(1)
    if key == ord('q'):
        break

cv.destroyAllWindows
cap.release()
