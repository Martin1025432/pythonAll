# -*- coding: utf-8 -*-
"""
Created on Mon Apr  2 10:06:27 2018

@author: Administrator
"""
import numpy as np
from PIL import Image
import cv2

img=cv2.imread("a3.tif",-1)
print(img)
##img=cv2.cvtColor(imgd,cv2.COLOR_BGR2RGB)
##while(1):
##    cv2.imshow("image", imgd)
##    cv2.waitKey(0)
##    break
y=len(img)
x=len(img[0])
b=img
g=img*100
r=img*200
#
#b = np.zeros((img.shape[0],img.shape[1]), dtype=img.dtype) 
#g = np.zeros((img.shape[0],img.shape[1]), dtype=img.dtype) 
#r = np.zeros((img.shape[0],img.shape[1]), dtype=img.dtype) 
#
#s1=int(np.max(img)/5*1)
#s2=int(np.max(img)/5*2)
#s3=int(np.max(img)/5*3)
#s4=int(np.max(img)/5*4)
#s5=np.max(img)
#print(s1,s2,s3,s4,s5)

#for k in range(len(img)):
#    a1=img[k]
#    for i in range(len(a1)):
#        if a1[i]=
#        a1[i] = [100,255][a1[i]<50]

#for j iin range(x-1):
#    print(img[x])
#print(a)        
#for j in range(y):
#    for i in range(x):
#        if (img[j][i] <= s1) : 
#            b[j][i] = 65500
#            g[j][i] = img[j][i] * 5
#            r[j][i] = 0  
#                        
#        else:
#            if (img[j][i] <= s2):  
#                img[j][i] -= s1
#                b[j][i] = 65500-img[j][i]*5
#                g[j][i] = 65500
#                r[j][i] = 0 
#            else: 
#                if (img[j][i] <= s3): 
#                    img[j][i] -= s2
#                    b[j][i] = 0
#                    g[j][i] = 65500
#                    r[j][i] = img[j][i] * 5 
#                else: 
#                    if (img[j][i] <= s4) : 
#                        img[j][i] -= s3
#                        b[j][i] = 0
#                        g[j][i] =int(65500- img[j][i] * 32000/s1)
#                        r[j][i] = 65500
#                    else: 
#                        if (img[j][i] <= s5) : 
#                            img[j][i] -= s4
#                            b[j][i] = 0
#                            g[j][i] = int(32000-img[j][i] * 32000/s1)
#                            r[j][i] = 65500
       
##        b[j][i]=abs(6500-img[j][i])
##        g[j][i]=abs(3200-img[j][i])
##        r[j][i]=abs(0-img[j][i])
#merged = cv2.merge([b,g,r])
mergedByNp = np.dstack([b,g,r])  
cv2.imwrite("aa.tif", mergedByNp) 
#cv2.namedWindow('good', cv2.WINDOW_NORMAL)   
#while(1):
#    cv2.imshow("good", mergedByNp)
#    cv2.waitKey(0)
#    break