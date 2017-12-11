"""
cv2.Canny(image, threshold1, threshold2[, edges[, apertureSize[, L2gradient]]]) → edges
（1）其中较大的threshold2用于检测图像中明显的边缘，
但一般情况下检测的效果不会那么完美，边缘检测出来是
断断续续的，所以这时候用较小的threshold1用于将这些
间断的边缘连接起来。
"""

'''
HoughLinesP(InputArray image,OutputArray lines, double rho, double theta, int threshold, double minLineLength=0,double maxLineGap=0 )
image为输入图像，要求是8位单通道图像
lines为输出的直线向量，每条线用4个元素表示，即直线的两个端点的4个坐标值
rho和theta分别为距离和角度的分辨率
threshold为阈值，即步骤3中的阈值
minLineLength为最小直线长度，在步骤5中要用到，即如果小于该值，则不被认为是一条直线
'''

import numpy as np
import cv2
import math
img = cv2.imread('test3.jpeg')
#转换为灰度图
gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
#获取图像属性
print ('获取图像大小: ')


print (gray.shape)

imgray=gray.copy()
ret,thresh = cv2.threshold(imgray,210,255,0)
image ,contours,hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
cv2.rectangle(imgray,(0,0),(2592,1944),(0,0,0),-1)
for i in range(len(contours)):
    imag = cv2.drawContours(imgray,contours,i,(255,255,255),1)
"""
image ,contours,hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
#清空图片
cv2.rectangle(imgray,(0,0),(2592,1944),(0,0,0),-1)
#画出筛选轮廓
for i in range(len(contours)):
    imag = cv2.drawContours(imgray,contours,i,(255,255,255),1)
"""



## Apply edge detection method on the image
#edges = cv2.Canny(gray,255,255,apertureSize = 3)
cv2.rectangle(imgray,(1300,0),(2592,1944),(0,0,0),-1)
# This returns an array of r and theta values
lines = cv2.HoughLines(imgray,1,np.pi/180, 120)
lines2 = cv2.HoughLinesP(imgray,1,np.pi/180,30,minLineLength=100,maxLineGap=10)
# The below for loop runs till r and theta values 
# are in the range of the 2d array

"""

for i in range(len(lines)):
    for r,theta in lines[i]:

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
"""





for i in range(len(lines2)):
   
    x1=lines2[i][0][0]
    y1=lines2[i][0][1]
    x2=lines2[i][0][2]
    y2=lines2[i][0][3]    

    cv2.line(img,(x1,y1), (x2,y2), (0,0,255),2)

angle=math.atan((y2-y1)/(x2-x1)*180/(math.pi))

cv2.imwrite('houghlines3.jpg', img)
cv2.namedWindow("R",cv2.WINDOW_NORMAL);
cv2.imshow('R',imgray)

cv2.waitKey(0)
cv2.destroyAllWindows()

