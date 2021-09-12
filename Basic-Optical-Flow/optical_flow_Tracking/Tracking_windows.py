# import the necessary packages
import cv2 as cv 
import numpy as np
# now let's initialize the list of reference point
ref_point = []
click = False
points =()


cap = cv.VideoCapture(0)
_, frame = cap.read()
old_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

lk_params = dict(winSize=(20, 20),
                 maxLevel=4,
                 criteria=(cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT, 10, 0.01))

def shape_selection(event, x, y, flags, param):
    # grab references to the global variables
    global ref_point, click, points, point_selected, old_points
    cv.circle(frame, (x,y), 3, (0,200,255), 2)
    points =(x,y)

    # if the left mouse button was clicked, record the starting
    # (x, y) coordinates and indicate that cropping is being performed
    if event == cv.EVENT_LBUTTONDOWN:
        ref_point = [(x, y)]
        # old_points = [(x, y)]
        old_points = np.array([[x, y]], dtype=np.float32)
        click=True
    

    # check to see if the left mouse button  was released
    elif event == cv.EVENT_LBUTTONUP:
        click = False
        # record the ending (x, y) coordinates and indicate that
        # the cropping operation is finished
        ref_point.append((x, y))
        old_points = np.array([[ref_point[0], ref_point[1]]], dtype=np.float32)


        # draw a rectangle around the region of interest
        cv.rectangle(frame, ref_point[0], ref_point[1], (0, 255, 0), 2)

        cv.imshow("image", frame)
    

    # print(down)
    

cap =cv.VideoCapture(0)
cv.namedWindow("image")
cv.setMouseCallback("image", shape_selection)
point_selected = False
points = [()]
old_points = np.array([[]])


# keep looping until the 'q' key is pressed
while True:
    ret, frame = cap.read()
    cv.imshow('old frame ', old_gray)
    gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    # display the image and wait for a keypress
    clone = frame.copy()

    
    if click:
        cv.rectangle(frame, ref_point[0], points, (255, 0, 244), 2)

    key = cv.waitKey(1) & 0xFF
    print(len(ref_point))
    if len(ref_point)==2:
        cv.circle(frame, points, 5, (155, 0, 255), -1)
        new_points, status, error = cv.calcOpticalFlowPyrLK(
        old_gray, gray_frame, old_points, None, **lk_params)
        # print('drawing')
        cv.rectangle(frame, ref_point[0], ref_point[1], (200, 255, 0), 2)
        old_points = new_points 
        new_points=new_points.astype(int)
        print((new_points[0][1]))


        # p1 = new_points[0]
        # p2 = new_points[1]
        # print(p1, p2)

        # values = [p for p in new_points]
        # print(values)
        # x, y = new_points.ravel()
        cv.circle(frame, new_points[0][1], 8, (0, 255, 255), 4)
        cv.circle(frame, new_points[0][0], 8, (0, 255, 0), 4)
        cv.rectangle(frame, new_points[0][0], new_points[0][1], (0, 255, 0), 2)

        # cv.circle(image, ref_point[0], 3, (0,200,0), 2)
        # cv.circle(image, ref_point[1], 3, (0,200,0), 2)
        # cv.circle(image, (ref_point[1][0], ref_point[0][1]), 3, (0,200,0), 2)
        # cv.circle(image, (ref_point[0][0], ref_point[1][1]), 3, (0,200,0), 2)
    old_gray = gray_frame.copy()
    # press 'r' to reset the window
    if key == ord("r"):
        frame = clone.copy()

    # if the 'c' key is pressed, break from the loop
    elif key == ord("q"):
        break
    cv.imshow("image", frame)


# close all open windows
cv.destroyAllWindows()  