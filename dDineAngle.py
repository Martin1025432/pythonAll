"""
cv2.Canny(image, threshold1, threshold2[, edges[, apertureSize[, L2gradient]]]) → edges
（1）其中较大的threshold2用于检测图像中明显的边缘，
但一般情况下检测的效果不会那么完美，边缘检测出来是
断断续续的，所以这时候用较小的threshold1用于将这些
间断的边缘连接起来。
"""


import numpy as np
import cv2






img = cv2.imread('test6.jpeg')

#转换为灰度图
gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
#获取图像属性
print ('获取图像大小: ')
print (gray.shape)
# Apply edge detection method on the image
edges = cv2.Canny(gray,255,255,apertureSize = 3)
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
    
cv2.imwrite('houghlines3.jpg', img)

cv2.imshow('R',edges)
cv2.namedWindow('R',cv2.WINDOW_NORMAL)
cv2.waitKey(0)
cv2.destroyAllWindows()

