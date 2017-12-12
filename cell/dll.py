# -*- coding: utf-8 -*-
"""
Created on Tue Dec 12 23:40:58 2017

@author: Administrator
"""
import numpy as np
import cv2

def findEdge(a,b,dstImg,proImg):
    global imag,moment,mc,contours,hierarchy,mg,center,crop_img,thresh,mg_long,rmg,x,y
#    img = cv2.imread('test0.jpeg')
    imgray = cv2.cvtColor(proImg,cv2.COLOR_BGR2GRAY)
    ret,thresh = cv2.threshold(imgray,a,b,0)
    print("img trans done")
    image ,contours,hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    print("contours finded:",len(contours))


    if len(contours)>0:
        try:
            
    #轮廓周长 ,long所有轮廓的周长               
            long = [cv2.arcLength(contours[i],True) for i in range(len(contours)) ]
    #轮廓周长 ，mg_long,满足周长条件的 “轮廓” lish索引值
            mg_long=[i for i in range(len(long)) if long[i]>500 and long[i]<900]
            print("long fined:",len(mg_long))
    #计算轮廓的的矩
            moment=[cv2.moments(contours[i])for i in mg_long]
    #用面积筛选轮廓，找出大于100的轮廓索引值，mg，满足面积的周长list中的索引值
            mg=[i for i in range(len(moment)) if moment[i]['m00']>9000 and moment[i]['m00']<20000]
    #rmg,满足周长和面积的轮廓index
            rmg=[mg_long[i] for i in mg]
            print("s finded:",len(mg))            

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

