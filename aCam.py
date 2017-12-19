# -*- coding: utf-8 -*-
"""
Created on Thu Nov 30 17:50:24 2017

@author: Administrator
"""

import cv2
import numpy as np  
#cv2.namedWindow("img", cv2.WND_PROP_FULLSCREEN)
#cv2.setWindowProperty("img", cv2.WND_PROP_FULLSCREEN, cv2.CV_WINDOW_FULLSCREEN)
cap = cv2.VideoCapture(0)
#cap.set(3,2592)   
#cap.set(4,1944)  
#cap.set(3,1440)   
#cap.set(4,1080)  

cv2.namedWindow("img",cv2.WINDOW_NORMAL);  
#print (frame.shape)
while(1):
# get a frame
    ret, frame = cap.read()
# show a frame
    image=frame.copy()
    cv2.line(frame,(0,972), (2592,972), (0,0,255),2)
    cv2.line(frame,(1296,0), (1296,1944), (0,0,255),2)
    cv2.imshow("img", frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print (frame.shape)
        cv2.imwrite("apple2.jpeg", image)
        break
    
    
    
cap.release()
cv2.destroyAllWindows()