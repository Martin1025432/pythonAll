# -*- coding: utf-8 -*-
"""
Created on Sat Dec  9 11:54:11 2017

@author: Administrator
"""
import numpy as np
import cv2
img = cv2.imread('test3.jpeg')
crop_img = img.copy()

while(1):
    cv2.imshow('image',img)
    k = cv2.waitKey(1) & 0xFF
    if k == ord('q') :
        break
    if k == ord('a') :
        

        
cv2.destroyAllWindows()