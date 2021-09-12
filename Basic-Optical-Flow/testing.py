# import the necessary packages
import cv2

# now let's initialize the list of reference point
ref_point = []
click = False
points =()
def shape_selection(event, x, y, flags, param):
    # grab references to the global variables
    global ref_point, crop, click, points
    cv2.circle(image, (x,y), 3, (0,200,255), 2)
    points =(x,y)

    # if the left mouse button was clicked, record the starting
    # (x, y) coordinates and indicate that cropping is being performed
    if event == cv2.EVENT_LBUTTONDOWN:
        ref_point = [(x, y)]
        click=True

    # check to see if the left mouse button was released
    elif event == cv2.EVENT_LBUTTONUP:
        click = False
        # record the ending (x, y) coordinates and indicate that
        # the cropping operation is finished
        ref_point.append((x, y))

        # draw a rectangle around the region of interest
        cv2.rectangle(image, ref_point[0], ref_point[1], (0, 255, 0), 2)

        cv2.imshow("image", image)
    

    # print(down)
    

cap =cv2.VideoCapture(0)
cv2.namedWindow("image")
cv2.setMouseCallback("image", shape_selection)


# keep looping until the 'q' key is pressed
while True:
    ret, image = cap.read()
    # display the image and wait for a keypress
    clone = image.copy()
    if click:
        cv2.rectangle(image, ref_point[0], points, (255, 0, 244), 2)

    key = cv2.waitKey(1) & 0xFF
    print(len(ref_point))
    if len(ref_point)==2:
        # print('drawing')
        cv2.rectangle(image, ref_point[0], ref_point[1], (200, 255, 0), 2)
        # cv2.circle(image, ref_point[0], 3, (0,200,0), 2)
        # cv2.circle(image, ref_point[1], 3, (0,200,0), 2)
        # cv2.circle(image, (ref_point[1][0], ref_point[0][1]), 3, (0,200,0), 2)
        # cv2.circle(image, (ref_point[0][0], ref_point[1][1]), 3, (0,200,0), 2)

    # press 'r' to reset the window
    if key == ord("r"):
        image = clone.copy()

    # if the 'c' key is pressed, break from the loop
    elif key == ord("c"):
        break
    cv2.imshow("image", image)


# close all open windows
cv2.destroyAllWindows() 