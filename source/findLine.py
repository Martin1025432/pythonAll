# -*- coding: utf-8 -*-
"""
Created on Thu Dec  7 19:09:09 2017

@author: Administrator

cv2.Canny(image, threshold1, threshold2[, edges[, apertureSize[, L2gradient]]]) → edges

（1）其中较大的threshold2用于检测图像中明显的边缘，
但一般情况下检测的效果不会那么完美，边缘检测出来是
断断续续的，所以这时候用较小的threshold1用于将这些
间断的边缘连接起来。

（2）可选参数apertureSize是Sobel算子的大小（默认值
为3），而参数L2gradient是一个布尔值，如果为真，则使
用更精确的L2范数进行计算（即两个方向的倒数的平方和再
开方），否则使用L1范数（直接将两个方向导数的绝对值相加）。
 cv2.HoughLines(edges,1,np.pi/180, 118)
函数将通过步长为1的半径和步长为π/180的角来搜索所有可能的直线。
最后一个参数是经过某一点曲线的数量的阈值，超过这个阈值，就表
示这个交点所代表的参数对(rho,
theta)在原图像中为一条直线。具体理论可参考这篇文章。


"""

# Python program to illustrate HoughLine
# method for line detection
import cv2
import numpy as np

# Reading the required image in 
# which operations are to be done. 
# Make sure that the image is in the same 
# directory in which this python program is
img = cv2.imread('xyz.jpg')

# Convert the img to grayscale
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

# Apply edge detection method on the image
edges = cv2.Canny(gray,50,150,apertureSize = 3)

# This returns an array of r and theta values
lines = cv2.HoughLines(edges,1,np.pi/180, 118)

# The below for loop runs till r and theta values 
# are in the range of the 2d array
for r,theta in lines[0]:

    # Stores the value of cos(theta) in a
    a = np.cos(theta)

    # Stores the value of sin(theta) in b
    b = np.sin(theta)

    # x0 stores the value rcos(theta)
    x0 = a*r

    # y0 stores the value rsin(theta)
    y0 = b*r

    # x1 stores the rounded off value of (rcos(theta)-1000sin(theta))
    x1 = int(x0 + 1000*(-b))

    # y1 stores the rounded off value of (rsin(theta)+1000cos(theta))
    y1 = int(y0 + 1000*(a))

    # x2 stores the rounded off value of (rcos(theta)+1000sin(theta))
    x2 = int(x0 - 1000*(-b))

    # y2 stores the rounded off value of (rsin(theta)-1000cos(theta))
    y2 = int(y0 - 1000*(a))

    # cv2.line draws a line in img from the point(x1,y1) to (x2,y2).
    # (0,0,255) denotes the colour of the line to be 
    #drawn. In this case, it is red. 
    cv2.line(img,(x1,y1), (x2,y2), (0,0,255),2)

# All the changes made in the input image are finally
# written on a new image houghlines.jpg
cv2.imwrite('houghlines3.jpg', img)