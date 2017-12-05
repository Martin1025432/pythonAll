# -*- coding: utf-8 -*-
"""
Created on Tue Nov 21 09:02:00 2017

@author: Administrator
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Nov 10 13:48:40 2017

@author: Administrator
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Nov  8 17:38:33 2017

@author: Administrator
"""

#coding:utf-8
#===============================================
#文件说明:
#       第三节:图像处理---之---在python下,怎样使用OpenCv设置ROI区域
#开发环境：
#       Ubuntu14.04+Python2.7+IDLE+IPL
#时间地点:
#       陕西师范大学　2016.11.19
#作　　者:
#       九月
#===============================================

#1--Python中ROI区域的设置也是使用Numpy中的索引来实现的
#import cv2
#import numpy as np
#import matplotlib.pyplot as plt 
##以灰度读取图片
##srcImg = cv2.imread("CZ180.jpg",0)
#srcImg = cv2.imread("CZ180.jpg")
#
#
##roiImag=srcImg[800:1200,0:800] 
#imgray = cv2.cvtColor(srcImg,cv2.COLOR_BGR2GRAY)#转成灰色图
#plt.imshow(imgray, cmap="gray")
#
##二值化 ,找轮廓前必须先把图像二值化    
#ret, gray = cv2.threshold(imgray, 150, 250, cv2.THRESH_BINARY)
#plt.imshow(gray)

#coding=utf-8  
import cv2  
import numpy as np    
  
img = cv2.imread("test3.jpeg", 0)  

circles= cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,1,100,param1=100,param2=20,minRadius=25,maxRadius=40)  
print(circles)
print(len(circles[0]))
for circle in circles[0]:
    #圆的基本信息
    print(circle[2])
    #坐标行列
    x=int(circle[0])
    y=int(circle[1])
    #半径
    r=int(circle[2])
    #在原图用指定颜色标记出圆的位置
    img=cv2.circle(img,(x,y),r,(0,0,255),5)
cv2.imshow('res',img)
cv2.waitKey(0)  
cv2.destroyAllWindows()   




#gradX = cv2.Sobel(gray, ddepth = cv2.CV_32F, dx = 1, dy = 0, ksize = -1)
#gradY = cv2.Sobel(gray, ddepth = cv2.CV_32F, dx = 0, dy = 1, ksize = -1)
#plt.imshow(gray)
##cv2.imshow("[sImg]",thresh)   
#找轮廓必须有三个返回值，网上教程大部份出错
#thresh,contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)  
