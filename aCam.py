# -*- coding: utf-8 -*-
"""
Created on Thu Nov 30 17:50:24 2017

@author: Administrator
"""

import cv2
import numpy as np  
cap = cv2.VideoCapture(0)
while(1):
# get a frame
    ret, frame = cap.read()
# show a frame
    cv2.imshow("capture", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.imwrite("tes6.jpeg", frame)
        break
cap.release()
cv2.destroyAllWindows()