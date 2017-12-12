# -*- coding: utf-8 -*-
"""
Created on Tue Dec 12 23:38:46 2017

@author: Administrator
"""

from dll import *
cv2.namedWindow("image",cv2.WINDOW_NORMAL)
img = cv2.imread('apple2.jpeg')
crop_img = img.copy()
cv2.line(img,(0,972), (2592,972), (0,0,255),2)
cv2.line(img,(1296,0), (1296,1944), (0,0,255),2)
cam(0)
while(1):
    cv2.imshow('image',img)
    k = cv2.waitKey(1) & 0xFF
    if k == ord('q') :
        break
    if k == ord('a') :
        
        ct=findEdge(150,255,img,crop_img)
#        cv2.imshow('image',thresh)
        
cv2.destroyAllWindows()