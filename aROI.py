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

def draw_circle(event,x,y,flags,param):
    global ix,iy,drawing,mode,x0,y0,x1,y1,img0,img

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix,iy=x,y
        x0,y0=x+5,y+5
        print(x,y)
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing == True:
            if mode == True:
                img = cv2.imread('test3.jpeg')
                cv2.rectangle(img,(ix,iy),(x,y),(0,255,0),2)
                pass
            else:
                cv2.circle(img,(x,y),5,(0,0,255),-1)
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        if mode == True:
#            cv2.rectangle(img,(ix,iy),(x,y),(0,255,0),-1)
            x1,y1=x-5,y-5
#            cv2.rectangle(img,(x0,y0),(x1,y1),(0,0,255),2) 
            crop_img = img[ y0:y1,x0:x1,]
            cv2.imwrite("test0.jpeg", crop_img)
            print(x,y)
        else:
            cv2.circle(img,(x,y),5,(0,0,255),-1)
    elif event == cv2.EVENT_RBUTTONDOWN:
        img = cv2.imread('test3.jpeg')
img = cv2.imread('test3.jpeg')

#gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
#gray = np.float32(gray)
            
#img = np.zeros((512,512,3),np.uint8)
cv2.namedWindow('image')
cv2.setMouseCallback('image',draw_circle)


while(1):
    cv2.imshow('image',img)
    k = cv2.waitKey(1) & 0xFF
    if k == ord('q') :
        break
cv2.destroyAllWindows()