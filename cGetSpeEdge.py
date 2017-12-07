# -*- coding: utf-8 -*-
"""
Created on Tue Dec  5 18:04:35 2017

@author: Administrator
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Dec  4 21:18:37 2017

@author: Administrator
"""
"""CV_EVENT_MOUSEMOVE 0             滑动  
CV_EVENT_LBUTTONDOWN 1           左键点击  
CV_EVENT_RBUTTONDOWN 2           右键点击  
CV_EVENT_MBUTTONDOWN 3           中间点击  
CV_EVENT_LBUTTONUP 4             左键释放  
CV_EVENT_RBUTTONUP 5             右键释放  
CV_EVENT_MBUTTONUP 6             中间释放  
CV_EVENT_LBUTTONDBLCLK 7         左键双击  
CV_EVENT_RBUTTONDBLCLK 8         右键双击  
CV_EVENT_MBUTTONDBLCLK 9         中间释放 
"""
import numpy as np
import cv2

drawing = False #鼠标按下为真
mode = True #如果为真，画矩形，按m切换为曲线
ix,iy=-1,-1
def findEdge(a,b):
    global imag,moment,mc,contours,hierarchy,mg
    global imag,moment,mc,contours,hierarchy,mg,center
#    img = cv2.imread('test0.jpeg')
    imgray = cv2.cvtColor(crop_img,cv2.COLOR_BGR2GRAY)
    ret,thresh = cv2.threshold(imgray,a,b,0)
    image ,contours,hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
#计算轮廓的的矩
    if len(contours)>0:
        try:
            moment=[cv2.moments(contours[i])for i in range(len(contours))]
#用面积筛选轮廓，找出大于100的轮廓索引值
            mg=[i for i in range(len(moment)) if moment[i]['m00']>100 and moment[i]['m00']<20000]
#画出筛选轮廓
            for i in mg:
                imag = cv2.drawContours(crop_img,contours,i,(236,0,0),1)
#画出最小外接圆                
            (x,y),radius = cv2.minEnclosingCircle(contours[mg[0]])
            center = (int(x),int(y))
            radius = int(radius)
            imgdd = cv2.circle(crop_img,center,radius,(0,255,0),2)
#找出筛选轮廓重心点   
#            mc=[(moment[i]['m10']/moment[i]['m00'],moment[0]['m01']/moment[0]['m00'])for i in mg]
            
#画出中心点
#            for i in range(0,len(mc)):        
#                cv2.circle(crop_img,(int(mc[i][0]),int(mc[i][1])),2,(0,0,255),-1)                  
#            print("重心:",mc)
#画出最小外接圆中心
            cv2.circle(crop_img,center,2,(0,255,0),-1)                  
            print("虚拟中心:",center)            
        except:
             print("no contours")       
    else:
        print("I can't find the contours")
    
def draw_circle(event,x,y,flags,param):
    global ix,iy,drawing,mode,x0,y0,x1,y1,img0,img,crop_img

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix,iy=x,y
        x0,y0=x,y
        print(x,y)
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing == True:
            if mode == True:
                img = cv2.imread('test3.jpeg')
                cv2.rectangle(img,(ix,iy),(x,y),(0,255,0),2)
                pass

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        if mode == True:
            img = cv2.imread('test3.jpeg')

            x1,y1=x,y
            cv2.rectangle(img,(x0,y0),(x1,y1),(0,0,255),2) 
#            crop_img = img[ y0:y1,x0:x1]
            crop_img = img
            cv2.imwrite("test0.jpeg", crop_img)
            print(x,y)

    elif event == cv2.EVENT_RBUTTONDOWN:
        img = cv2.imread('test3.jpeg')
    
         
        
        
img = cv2.imread('test3.jpeg')

#gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
#gray = np.float32(gray)
            
#img = np.zeros((512,512,3),np.uint8)
cv2.namedWindow('image')
cv2.setMouseCallback('image',draw_circle)
#crop_img = img[ 142:327,305:520]
#crop_img = img[ y0:y1,x0:x1]
crop_img = img

while(1):
    cv2.imshow('image',img)
    k = cv2.waitKey(1) & 0xFF
    if k == ord('q') :
        break
    if k == ord('a') :
        
        findEdge(160,100)
cv2.destroyAllWindows()