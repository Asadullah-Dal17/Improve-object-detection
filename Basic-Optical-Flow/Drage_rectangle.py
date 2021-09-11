import cv2 as cv 
import numpy as np  
import copy

Draw = False
mode = True
ix, iy =-1,-1


image = cv.imread("image.jpg")
def GetPoints(event, x,y,flags,  param ):
    global Draw, ix, iy, mode
    if event == cv.EVENT_LBUTTONDBLCLK:
        cv.circle(image,(x,y),5,(255,0,0),-1)
        # fourPoint.append((x,y))
        Draw =True
        ix, iy =x, y 
    elif event==cv.EVENT_MOUSEMOVE:
        if Draw ==False:
            if mode ==True:
                cv.rectangle(image, (ix, iy), (x,y), (0,233,255), 1)
            else:
                cv.circle(image, (x,y), 5, (0,0,255), -1)
    elif event ==cv.EVENT_LBUTTONUP:
        Draw = False
        if mode==True:
            cv.rectangle(image, (ix,iy), (x,y),(0,255,0), 1)
        else:
            cv.circle(image, (x,y), 5, (0,255,0), -1)

        print(x,y)
    

cv.namedWindow("image", cv.WINDOW_AUTOSIZE)
cv.setMouseCallback('image',GetPoints)

while True:
    
    CopyImage = copy.copy(image)
    # print(type(CopyImage))
    # cv.imshow("imagcopy", CopyImage)
    # print(fourPoint)
    
    cv.imshow("image", CopyImage)
    Key = cv.waitKey(1)
    if Key ==ord("m"):
        mode =not mode
    if Key ==ord('q'):

        break
cv.destroyAllWindows()