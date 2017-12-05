# -*- coding: utf-8 -*-
"""
Created on Sat Dec  2 14:09:32 2017

@author: Administrator
"""

# coding=utf-8
import cv2
import numpy as np


'''Harris算法角点特征提取'''

img = cv2.imread('test0.jpeg')
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
gray = np.float32(gray)

# {标记点大小，敏感度（3~31,越小越敏感）}
# OpenCV函数cv2.cornerHarris() 有四个参数 其作用分别为 :
#img - Input image, it should be grayscale and float32 type.
#blockSize - It is the size of neighbourhood considered for corner detection
#ksize - Aperture parameter of Sobel derivative used.
#k - Harris detector free parameter in the equation,在0.04 到0.05之间
dst = cv2.cornerHarris(gray,1,6,0.05)
img[dst>0.01 * dst.max()] = [0,0,255]

cv2.imshow('corners',img)
cv2.waitKey()
cv2.destroyAllWindows()