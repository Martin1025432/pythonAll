# -*- coding: utf-8 -*-
"""
Created on Thu Dec  7 17:56:06 2017

@author: Administrator
"""

import numpy as np
import cv2






img = cv2.imread('test3.jpeg')

#转换为灰度图
gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
#获取图像属性
print ('获取图像大小: ')
print (gray.shape)
#转换为矩阵
m = np.matrix(gray)

delta_h = m
#计算x方向的梯度的函数（水平方向锐化算子）
def findAngle():
    pass
def grad_x(h):
    a = int(h.shape[0])
    b = int(h.shape[1])

    for i in range(a):
        for j in range(b):
            if i-1>=0 and i+1<a and j-1>=0 and j+1<b:
                c = abs(int(h[i-1,j-1]) - int(h[i+1,j-1]) + 2*(int(h[i-1,j]) - int(h[i+1,j])) + int(h[i-1,j+1]) - int(h[i+1,j+1]))
#                print c
                if c>255:
#                    print c
                    c = 255
                delta_h[i,j] = c
            else:
                delta_h[i,j] = 0
    print ('x方向的梯度:', delta_h)
    return delta_h
##计算y方向的梯度的函数（水平方向锐化算子）
def grad_y(h):
    a = int(h.shape[0])
    b = int(h.shape[1])

    for i in range(a):
        for j in range(b):
            if i-1>=0 and i+1<a and j-1>=0 and j+1<b:
                c = abs(int(h[i-1,j-1]) - int(h[i-1,j+1]) + 2*(int(h[i,j-1]) - int(h[i,j+1])) + (int(h[i+1,j-1]) - int(h[i+1,j+1])))  #注意像素不能直接计算，需要转化为整型
#                print c
                if c > 255:
                    c = 255
                delta_h[i,j] = c
            else:
                delta_h[i,j] = 0
    print ('y方向的梯度：' ,delta_h)
    return delta_h

# Laplace 算子  
img_laplace = cv2.Laplacian(gray, cv2.CV_64F, ksize=3)  

dx = np.array(grad_x(gray))
dy = np.array(grad_y(gray))

#dxy = dx + dy
#print 'dxy1:'
#print dxy

A = dx * dx
B = dy * dy 
C = dx * dy

print ('A1=',A,'B=',B,'C=',C)


A1 = A
B1 = B
C1 = C

A1 = cv2.GaussianBlur(A1,(5,5),1.5)
B1 = cv2.GaussianBlur(B1,(5,5),1.5)
C1 = cv2.GaussianBlur(C1,(5,5),1.5)

print ('A1=',A1,'B1=',B1,'C1=',C1)

a = int(gray.shape[0])
b = int(gray.shape[1])

R = np.zeros(gray.shape)
for i in range(a):
    for j in range(b):
        M = [[A1[i,j],C1[i,j]],[C1[i,j],B1[i,j]]]

        R[i,j] = np.linalg.det(M) - 0.06 * (np.trace(M)) * (np.trace(M))

print ('R=',R)
cv2.imshow('R',R)
cv2.namedWindow('R',cv2.WINDOW_NORMAL)
cv2.waitKey(0)
cv2.destroyAllWindows()

