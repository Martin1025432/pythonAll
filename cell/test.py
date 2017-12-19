# -*- coding: utf-8 -*-
"""
Created on Wed Dec 20 00:12:05 2017

@author: Administrator
"""
from dll import *
#cv2.namedWindow('good', cv2.WINDOW_AUTOSIZE)

img=cv2.imread('apple2.jpeg')
imgg=img.copy()
try:
    findEdge(150,255,imgg,img,540,550,9000,20000)
    cv2.namedWindow('good', cv2.WINDOW_NORMAL)
    while(1):
    
        cv2.imshow('good',imgg)
        cv2.waitKey(0)
        break
    cv2.destroyAllWindows()
except:
    pass
