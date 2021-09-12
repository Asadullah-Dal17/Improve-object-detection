import numpy as np
import cv2
tracker = cv2.TrackerKCF_create()
video = cv2.VideoCapture(0)
ok,frame=video.read()




while True:
	ret,frame=video.read()
	if not ret:
		break
	bbox = cv2.selectROI(frame)
	print(bbox)

	ok = tracker.init(frame,bbox)
	print('testing')
	ok,bbox=tracker.update(frame)
	if ok:
	     (x,y,w,h)=[int(v) for v in bbox]
	     cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2,1)
	else:
	    cv2.putText(frame,'Error',(100,0),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)
	cv2.imshow('Tracking',frame)
	if cv2.waitKey(1) & 0XFF==27:
		break
cv2.destroyAllWindows()