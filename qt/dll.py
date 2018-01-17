# -*- coding: utf-8 -*-
"""
Created on Tue Dec 12 23:40:58 2017

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
import threading
from cSharpDll import *


def drawCircle(img):
    a=tool.find()
    x=a[0]
    y=a[1]
    r=a[2]
    imgray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    cv2.circle(img,(int(x),int(y)),int(r),(0,255,0),10)


def findEdge(a,b,dstImg,proImg,minLong,maxLong,minS,MaxS):
#    global imag,moment,mc,contours,hierarchy,mg,center,crop_img,thresh,mg_long,rmg,x,y
#    img = cv2.imread('test0.jpeg')
    imgray = cv2.cvtColor(proImg,cv2.COLOR_BGR2GRAY)
    ret,thresh = cv2.threshold(imgray,a,b,0)
    print("完成二值处理")
    image ,contours,hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    
    print("找到轮廓数量:",len(contours))


    if len(contours)>0:
        try:
            
    #轮廓周长 ,long所有轮廓的周长               
            long = [cv2.arcLength(contours[i],True) for i in range(len(contours)) ]
    #轮廓周长 ，mg_long,满足周长条件的 “轮廓” lish索引值
            mg_long=[i for i in range(len(long)) if long[i]>minLong and long[i]<maxLong]
            print("满足周长条件数量:",len(mg_long))
            cText="perimeter finded:"+str(len(mg_long))
    #计算轮廓的的矩
            moment=[cv2.moments(contours[i])for i in mg_long]
    #用面积筛选轮廓，找出大于100的轮廓索引值，mg，满足面积的周长list中的索引值
            mg=[i for i in range(len(moment)) if moment[i]['m00']>minS and moment[i]['m00']<MaxS]
    #rmg,满足周长和面积的轮廓index
            rmg=[mg_long[i] for i in mg]
            print("满足面积数量:",len(mg))            
            sText="area finded:"+str(len(mg))
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
            cv2.putText(dstImg,cText,(10,200),cv2.FONT_HERSHEY_COMPLEX,3,(0,0,255),5)
            cv2.putText(dstImg,sText,(10,300),cv2.FONT_HERSHEY_COMPLEX,3,(0,0,255),5)
            print("虚拟中心:",center)            
        except:
             print("no contours")       
    else:
        print("I can't find the contours")
    return  center   

def cam(number):

    try:
        cap = cv2.VideoCapture(number)
        cap.set(3,2592)   
        cap.set(4,1944)  
        ret, frame = cap.read() 
        print("camer",number,"is ok")
    except:
        print("camer",number,"is fail")
    return frame

def findEdgeCanny(a,b,dstImg,proImg):
    pass
global nData,pData,nSoc,pSoc 
nData='none'
pData='none'
nSoc=socket(AF_INET, SOCK_STREAM)
pSoc=socket(AF_INET, SOCK_STREAM)

def server(serverAddr,nClientIP,pClientIP):
    global nData,pData,nSoc,pSoc 
    serverSoc = socket(AF_INET, SOCK_STREAM)
    serverSoc.bind(serverAddr)
    serverSoc.listen(5)
    while True:
    # 接受一个新连接:
        sock, addr = serverSoc.accept()
        if(addr[0]==nClientIP):
    # 创建新线程来处理TCP连接:
            print(sock)
            nData='conned'
            nSoc=sock            
            t = threading.Thread(target=tcplink, args=(sock, addr,nClientIP,pClientIP))
            t.start()
            print('nclien'+nData)
        if(addr[0]==pClientIP):
    # 创建新线程来处理TCP连接:
            print(addr)
            pData='conned'
            pSoc=sock   
            t = threading.Thread(target=tcplink, args=(sock, addr,nClientIP,pClientIP))
            t.start()  
            print('pclien'+pData)

def tcplink(sock, addr,nClientIP,pClientIP):
    global nData,pData,nSoc,pSoc 
    while True:
        try:
            data = sock.recv(1024)
            if(data!=''):
                if(addr[0]==nClientIP):
                   nData=data
                   print(nData)
                if(addr[0]==pClientIP):
                   nData=data                 
                
            if data == 'exit' or not data:
                break
        except:
            print('error')
    sock.close()
    print ('Connection from closed.')
    

     
    
    
    