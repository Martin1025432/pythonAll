# -*- coding: utf-8 -*-
"""
Created on Thu Nov 30 17:50:24 2017

@author: Administrator
"""

import cv2
import numpy as np  
#cv2.namedWindow("img", cv2.WND_PROP_FULLSCREEN)
#cv2.setWindowProperty("img", cv2.WND_PROP_FULLSCREEN, cv2.CV_WINDOW_FULLSCREEN)
cap1 = cv2.VideoCapture(0)
#cap2 = cv2.VideoCapture(1)
#cap1.set(3,2592)   
#cap1.set(4,1944) 

#cap2 = cv2.VideoCapture(1)
#cap2.set(3,2592)   
#cap2.set(4,1944) 


 
#cap.set(3,1440)   
#cap.set(4,1080)  

#cv2.namedWindow("img",cv2.WINDOW_NORMAL);  
#print (frame.shape)
while(1):
# get a frame
    ret1, frame1 = cap1.read()
    
#    ret2, frame2 = cap2.read()    
# show a frame
#    image1=frame1.copy()
#    image2=frame1.copy()
#    cv2.line(frame1,(0,972), (2592,972), (0,0,255),2)
#    cv2.line(frame,(1296,0), (1296,1944), (0,0,255),2)
    cv2.imshow("img1", frame1)
#    cv2.imshow("img2", frame2) 
    print (frame1.shape)
#    print (frame2.shape)
    cv2.waitKey(0) 
    break
#    if cv2.waitKey(1) & 0xFF == ord('q'):
##        print (frame.shape)
##        cv2.imwrite("apple2.jpeg", image)
#        break
#    
    
    
cap1.release()
#cap2.release()
cv2.destroyAllWindows()