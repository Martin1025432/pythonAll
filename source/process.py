# -*- coding: utf-8 -*-
"""
Created on Tue Nov 28 19:20:55 2017

@author: Administrator
"""

import numpy as np
import cv2
#def findEdge(a,b):
#    global imag,img,imgray    
#    ret,thresh = cv2.threshold(imgray,a,b,0)
#    image ,contours,hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
###绘制独立轮廓，如第四个轮廓
#    imag = cv2.drawContours(img,contours,-1,(0,255,0),2)
#    
##但是大多数时候，下面方法更有用
##imag = cv2.drawContours(img,contours,3,(0,255,0),2)
#blackLevel=160
#whiteLevel=255
##findEdge(blackLevel,whiteLevel)
#adjustDone=0
img = cv2.imread('test3.jpeg')
#imgray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
ret,thresh = cv2.threshold(img,160,255,0)
image ,contours,hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
##绘制独立轮廓，如第四个轮廓
imag = cv2.drawContours(img,contours,-1,(0,255,0),2)
cv2.imshow('imfag',img)
while(1):
        if cv2.waitKey(1) == ord('q'):
            break    
#while(adjustDone==0):
#    while(adjustDone==0):
#        cv2.imshow('imag',imag)
#        if cv2.waitKey(1) == ord('q'):
#            adjustDone=1
#            break
#        if cv2.waitKey(1) == ord('w'):
#            if(blackLevel<245):
#                blackLevel=blackLevel+10
#            break
#        if cv2.waitKey(1) == ord('s'):
#            if(blackLevel>15):
#                blackLevel=blackLevel-10
#            break    
#        if cv2.waitKey(1) == ord('e'):
#            if(whiteLevel<245):
#                whiteLevel=whiteLevel+10
#            break    
#        if cv2.waitKey(1) == ord('d'):
#            if(whiteLevel>15):
#                whiteLevel=whiteLevel-10                
#            break
#    findEdge(blackLevel,whiteLevel)

cv2.destroyAllWindows() 
        
