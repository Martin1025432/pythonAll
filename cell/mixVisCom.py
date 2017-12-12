# -*- coding: utf-8 -*-
"""
Created on Tue Dec 12 11:14:28 2017

@author: Administrator
"""
from socket import socket, AF_INET , SOCK_STREAM,SOL_SOCKET,SO_SNDBUF
import time 
import win32api,win32con  
import sqlite3
import os, sys
import time
import numpy as np
import cv2
#from findEdge import *
cap = cv2.VideoCapture(0)
#相机像索设置
w=2592
h=1944
cap.set(3,w)   
cap.set(4,h)  
cv2.namedWindow("image",cv2.WINDOW_NORMAL)
#设置服务器地址
HOST = '192.168.0.30'                  #服务器IP
Port = 10001                           #端口号
Addr = (HOST,Port)                     #连接地址
Soc= socket(AF_INET , SOCK_STREAM)     #创建TCP/IP套接字
#Soc.setblocking(False)
def findEdge(a,b,dstImg,proImg):
    global imag,moment,mc,contours,hierarchy,mg,center,crop_img,thresh,mg_long,rmg,x,y
#    img = cv2.imread('test0.jpeg')
    imgray = cv2.cvtColor(proImg,cv2.COLOR_BGR2GRAY)
    ret,thresh = cv2.threshold(imgray,a,b,0)
    print("1")
    image ,contours,hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    print(len(contours))


    if len(contours)>0:
        try:
            
    #轮廓周长                
            long = [cv2.arcLength(contours[i],True) for i in range(len(contours)) ]

            mg_long=[i for i in range(len(long)) if long[i]>500 and long[i]<900]
    #计算轮廓的的矩
            moment=[cv2.moments(contours[i])for i in mg_long]
    #用面积筛选轮廓，找出大于100的轮廓索引值
            mg=[i for i in range(len(moment)) if moment[i]['m00']>9000 and moment[i]['m00']<20000]
            rmg=[mg_long[i] for i in mg]
            
            
            
#            moment=[cv2.moments(contours[i])for i in range(len(contours))]
#用面积筛选轮廓，找出大于100的轮廓索引值
#            mg=[i for i in range(len(moment)) if moment[i]['m00']>0 and moment[i]['m00']<113800]
#画出筛选轮廓
            for i in rmg:
                imag = cv2.drawContours(dstImg,contours,i,(236,0,0),5)
#画出最小外接圆                
            (x,y),radius = cv2.minEnclosingCircle(contours[rmg[0]])
            center = (int(x),int(y))
            radius = int(radius)
            imgdd = cv2.circle(dstImg,center,radius,(0,255,0),5)
#找出筛选轮廓重心点   
#           mc=[(moment[i]['m10']/moment[i]['m00'],moment[0]['m01']/moment[0]['m00'])for i in mg]
            
#画出中心点
#            for i in range(0,len(mc)):        
#                cv2.circle(crop_img,(int(mc[i][0]),int(mc[i][1])),2,(0,0,255),-1)                  
#            print("重心:",mc)
#画出最小外接圆中心
            cv2.circle(dstImg,center,5,(0,255,0),-1)
            centerText="X="+str(center[0])+",Y="+str(center[1])
            cv2.putText(dstImg,centerText,(10,100),cv2.FONT_HERSHEY_COMPLEX,3,(0,0,255),5)   
            print("虚拟中心:",center)            
        except:
             print("no contours")       
    else:
        print("I can't find the contours")
    

#画直线

#cv2.line(img,(0,972), (2592,972), (0,0,255),2)
#cv2.line(img,(1296,0), (1296,1944), (0,0,255),2)

#gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
#gray = np.float32(gray)            
#img = np.zeros((512,512,3),np.uint8)
def vision():
    global imgd
    ret, frame = cap.read()   
# show a frame
    crop_img = frame.copy() 
#   cv2.imwrite("apple3.jpeg", crop_img)
    imgd=frame.copy() 
    findEdge(130,255,imgd,crop_img)
while(1):
    try:
        Soc.connect(Addr)
        Soc.setblocking(False)
        print("conn done")
        break
    except:
        time.sleep(1)
        print("waiting robot power on") 
        
#vision()        
#cv2.imshow("image", imgd)       
#cv2.waitKey(0)       
        
        
imgd = cv2.imread('apple2.jpeg')        
while(1): 
       
    try:
#        print("waiting data")
        receiveStr=str(Soc.recv(1024))
        
       
        if receiveStr=="b'TRG\\r'":
            print(receiveStr)
            vision()
#            cv2.imshow("image", imgd)
            print(type(x))
            output=str(int(x))+','+str(int(y))
            Soc.send(bytes(output,'utf8'))
#            Soc.send(bytes(str(int(x)),'utf8'))
#            Soc.send(bytes(str(int(y)),'utf8'))


#        if receiveStr=='2'
    except:
#            print("error")
        pass

    cv2.imshow("image", imgd) 
    if cv2.waitKey(1) & 0xFF == ord('q'):
      

        break
cv2.destroyAllWindows()
#receiveStr=str(Soc.recv(1024))  
#if receiveStr=='' :      
#    Soc.send(bytes("1",'utf8'))
    

          
