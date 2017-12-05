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
import cv2
import numpy as np
import matplotlib.pyplot as plt 
#以灰度读取图片
#srcImg = cv2.imread("CZ180.jpg",0)
srcImg = cv2.imread("test3.jpeg")
plt.imshow(srcImg, cmap="gray")
#plt.imshow(srcImg, cmap="gray")

#cv2.imshow 必须跟随 cv2.waitKey(0)
#cv2.imshow("[srcImg]",srcImg)                  #[1]显示原始图片
#roiImag=srcImg[800:1200,0:800] 
imgray = cv2.cvtColor(srcImg,cv2.COLOR_BGR2GRAY)#转成灰色图
#srcImg[0:200,0:300]=roiImag
#plt.imshow(roiImag, cmap="gray")
#cv2.imshow("[srcImg]",srcImg)       
#cv2.waitKey(0)
#cv2.imshow("[srcImg]",roiImag)  

#二值化 ,找轮廓前必须先把图像二值化    
ret, thresh = cv2.threshold(imgray, 150, 250, cv2.THRESH_BINARY)
#cv2.imshow("[sImg]",thresh)   
#找轮廓必须有三个返回值，网上教程大部份出错
thresh,contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)  
##plt.imshow(roiImag, cmap="gray")
#函数cv2.drawContours()可以被用来绘制轮廓。它可以根据你提供的边界点绘制任何形状。
"""
绘制轮廓
它的第一个参数是原始图像，
第二个参数是轮廓，一个python列表，
第三个参数是轮廓的索引（在绘制独立轮廓是很有用，当设置为-1时绘制所有轮廓）。
接下来的参数是轮廓的颜色和厚度。
"""
#在彩色图片上画线，才有颜色
#cv2.drawContours(roiImag,contours,-1,(0,0,255),2)  
#轮廓面积，即为车牌面积
#cv2.imshow("img", thresh)
#length=[cv2.contourArea(contours[i],True) for i in range(len(contours))] 
#a=length.index(max(length))
#cv2.drawContours(srcImg,contours,a,(0,0,255),2)  
#cv2.imshow("img1", roiImag)
#cnt=contours[1]
#perimeter = cv2.arcLength(cnt,True)
x,y,w,h=cv2.boundingRect(contours[0])
img=cv2.rectangle(srcImg,(x,y),(x+w,y+h),(0,255,0),2)
cv2.imshow("img2", thresh)  
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (50, 7))
closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
#腐蚀
closed = cv2.erode(closed, None, iterations = 10)
#膨胀
closed = cv2.dilate(closed, None, iterations = 15)

thresh2,contours, hierarchy = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
cv2.drawContours(srcImg,contours,-1,(0,0,255),2) 
cv2.imshow("imgD2", srcImg)  
#perimeter = cv2.arcLength(cnt,True)

#cv2.imshow("[sImg]",thresh)   
cv2.waitKey(0)